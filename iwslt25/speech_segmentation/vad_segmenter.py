from collections import deque
import os
import torch
from typing import Union
from simuleval.agents.actions import ReadAction
from simuleval.agents.states import AgentStates
import torchaudio
from ..speech_segmentation.speech_segmenter import SpeechSegmenter, TranslateAction


class VADSegmenter(SpeechSegmenter):

    def __init__(self, args):
        self.min_segment_length = args.min_segment_length
        self.max_segment_length = args.max_segment_length
        self.max_unvoiced_length = args.max_unvoiced_length
        self.voice_threshold = args.voice_threshold
        self.window_size_samples = args.window_size_samples
        self.sample_rate = args.sample_rate
        self.window_size_seconds = self.window_size_samples / self.sample_rate
        self.dump_audio_path = args.dump_audio_path
        self.dumped_audio_counter = 0

        self.model, utils = torch.hub.load(
            repo_or_dir="snakers4/silero-vad",
            model="silero_vad",
            force_reload=False,
            onnx=False,
        )

        (
            self.get_speech_timestamps,
            self.save_audio,
            self.read_audio,
            self.VADIterator,
            self.collect_chunks,
        ) = utils

    @staticmethod
    def add_args(parser):
        parser.add_argument(
            "--min-segment-length",
            type=float,
            default=2.0,
            help="Minimum segment length in seconds",
        )
        parser.add_argument(
            "--max-segment-length",
            type=float,
            default=20.0,
            help="Maximum segment length in seconds. Segments longer than this will be split into multiple segments.",
        )
        parser.add_argument(
            "--max-unvoiced-length",
            type=float,
            default=0.5,
            help="Maximum unvoiced length in seconds, segments longer that min_segment_length and with unvoiced length longer than this will be considered finished",
        )
        parser.add_argument(
            "--voice-threshold",
            type=float,
            default=0.5,
            help="Threshold for voice detection",
        )
        parser.add_argument(
            "--window-size-samples",
            type=int,
            default=512,
            help="VAD window size in samples",
        )
        parser.add_argument(
            "--sample-rate",
            type=int,
            default=16000,
            help="Sample rate of the audio",
        )
        parser.add_argument(
            "--dump-audio-path",
            type=str,
            default=None,
            help="Path to dump audio chunks; if None, no audio will be dumped",
        )

    def _ensure_state_attributes(self, states: AgentStates, reset=False):
        if not hasattr(states, "last_segment_position") or reset:
            states.last_segment_position = 0

        if not hasattr(states, "source_sample_rate") or reset:
            states.source_sample_rate = self.sample_rate

        if not hasattr(states, "last_vad_position") or reset:
            states.last_vad_position = 0

        if not hasattr(states, "vad_probs_deque") or reset:
            states.vad_probs_deque = deque()

        if not hasattr(states, "voiced_length_in_segment") or reset:
            states.voiced_length_in_segment = 0.0

        if not hasattr(states, "trailing_unvoiced_length") or reset:
            states.trailing_unvoiced_length = 0.0

        if not hasattr(states, "segment_length") or reset:
            states.segment_length = 0

    def _reset_state_for_segment(self, states: AgentStates):
        states.voiced_length_in_segment = 0.0
        states.trailing_unvoiced_length = 0.0
        states.segment_length = 0

    def _process_speech(self, states: AgentStates):
        t = torch.tensor(states.source[states.last_vad_position :], dtype=torch.float32)
        for i in range(0, len(t), self.window_size_samples):
            chunk = t[i : i + self.window_size_samples]
            if len(chunk) < self.window_size_samples:
                if states.source_finished:
                    chunk = torch.cat(
                        (chunk, torch.zeros(self.window_size_samples - len(chunk)))
                    )
                else:
                    break
            speech_prob = self.model(chunk, self.sample_rate).item()
            states.vad_probs_deque.append(speech_prob)
            states.last_vad_position += len(chunk)

    def policy(self, states: AgentStates) -> Union[TranslateAction, ReadAction]:
        assert states is not None
        self._ensure_state_attributes(states)
        self._process_speech(states)

        while len(states.vad_probs_deque) > 0:
            p = states.vad_probs_deque.popleft()
            if p > self.voice_threshold:
                states.voiced_length_in_segment += self.window_size_seconds
                states.trailing_unvoiced_length = 0
            else:
                states.trailing_unvoiced_length += self.window_size_seconds
            states.segment_length += self.window_size_samples

            if (
                states.segment_length / self.sample_rate >= self.min_segment_length
                and (
                    states.trailing_unvoiced_length >= self.max_unvoiced_length
                    or states.segment_length / self.sample_rate
                    >= self.max_segment_length
                )
            ):
                start = states.last_segment_position
                states.last_segment_position = end = min(start + states.segment_length, len(states.source))
                voiced = states.voiced_length_in_segment > 0
                self._reset_state_for_segment(states)
                if voiced:
                    finished = (
                        states.source_finished and len(states.vad_probs_deque) == 0
                    )
                    if start < end:
                        self._dump_audio(states, start, end)
                    if finished:
                        self._ensure_state_attributes(states, reset=True)
                    return TranslateAction(
                        states,
                        start,
                        end,
                        True,
                        finished,
                    )

        start = states.last_segment_position
        end = min(start + states.segment_length, len(states.source))
        if (
            states.segment_length * self.sample_rate >= self.min_segment_length
            and states.voiced_length_in_segment > 0
        ) or states.source_finished:
            if states.voiced_length_in_segment == 0:
                end = start
            finished = states.source_finished and len(states.vad_probs_deque) == 0
            if start < end:
                self._dump_audio(states, start, end)
            if finished:
                self._ensure_state_attributes(states, reset=True)
            return TranslateAction(
                states,
                start,
                end,
                finished,
                finished,
            )
        return ReadAction()

    def _dump_audio(self, states: AgentStates, start: int, end: int):
        if self.dump_audio_path is None:
            return
        if end - start > 0:
            if not os.path.exists(self.dump_audio_path):
                os.makedirs(self.dump_audio_path, exist_ok=True)
            self.dumped_audio_counter += 1
            start_s = start / self.sample_rate
            end_s = end / self.sample_rate
            audio_name = (
                f"segment_{self.dumped_audio_counter}_{start_s:.2f}_{end_s:.2f}.wav"
            )
            audio = states.source[start:end]
            torchaudio.save(
                os.path.join(self.dump_audio_path, audio_name),
                torch.tensor(audio, dtype=torch.float32).unsqueeze(0),
                self.sample_rate,
            )

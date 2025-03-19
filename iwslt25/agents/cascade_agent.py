import logging
from typing import Optional
from iwslt25.speech_segmentation.speech_segmenter import SpeechSegmenter, TranslateAction
from simuleval.agents.states import AgentStates
from simuleval.agents import SpeechToTextAgent
from simuleval.agents.actions import WriteAction, ReadAction

from faster_whisper import WhisperModel
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

import numpy as np

import torch

class CascadeAgent(SpeechToTextAgent):

    def __init__(self, args, segmenter : SpeechSegmenter):
        super().__init__(args)
        # set max thread to 1 to avoid deadlock
        torch.set_num_threads(1)
        assert segmenter is not None, "segmenter must be provided"
        self.device = args.device
        self.segmenter = segmenter
        self.segment_counter = 0
        self.step_length = args.step_length
        self.whisper_model = WhisperModel(
            model_size_or_path=args.whisper_model,
            device=self.device,
            compute_type="float16",
        )
        self.whisper_language = args.whisper_language
        self.translation_la_policy = args.translation_la_policy
        self.transcript_context = args.transcript_context
        self.translation_max_input_length_soft = args.translation_max_input_length_soft
        self.translation_max_input_length_hard = args.translation_max_input_length_hard

        self.translation_tokenizer = M2M100Tokenizer.from_pretrained(args.translation_model)
        self.translation_tokenizer.src_lang = self.whisper_language
        self.translation_tokenizer.tgt_lang = args.translation_language
        self.translation_model = M2M100ForConditionalGeneration.from_pretrained(args.translation_model).to(self.device).eval()

    @staticmethod
    def add_args(parser):
        """
        Add arguments to the parser
        """
        parser.add_argument(
            "--step-length",
            type=float,
            default=1.0,
        )
        parser.add_argument(
            "--whisper-model",
            choices=["small", "medium", "large", "large-v2", "large-v3", "large-v3-turbo"],
            default="large-v3-turbo",
        )
        parser.add_argument(
            "--whisper-task",
            choices=["transcribe", "translate"],
            default="transcribe",
        )
        parser.add_argument(
            "--whisper-language",
            type=str,
            default="en",
        )
        parser.add_argument(
            "--device",
            type=str,
            default="cpu",
        )
        parser.add_argument(
            "--translation-model",
            type=str,
            default="facebook/m2m100_418M",
        )
        parser.add_argument(
            "--translation-language",
            type=str,
            default="cs",
        )
        parser.add_argument(
            "--translation-la-policy",
            type=int,
            default=2,
            help="Translate every N tokens",
        )
        parser.add_argument(
            "--transcript-context",
            type=int,
            default=3,
            help="Number of previous words to keep in the transcript",
        )
        parser.add_argument(
            "--translation-max-input-length-soft",
            type=int,
            default=20,
            help="Maximum number of tokens to translate",
        )
        parser.add_argument(
            "--translation-max-input-length-hard",
            type=int,
            default=40,
            help="Maximum number of tokens to translate",
        )


    def _ensure_state_attributes(self, states: AgentStates, reset: bool = False):
        if not hasattr(states, "last_transcribed") or reset:
            states.last_transcribed = 0
        if not hasattr(states, "stable_transcript") or reset:
            states.stable_transcript = []
        if not hasattr(states, "transcript_hypothesis") or reset:
            states.transcript_hypothesis = []
        if not hasattr(states, "previous_segment_transcript") or reset:
            states.previous_segment_transcript = []
        if not hasattr(states, "stable_translation") or reset:
            states.stable_translation = []
        if not hasattr(states, "last_translated") or reset:
            states.last_translated = 0
        if not hasattr(states, "translation_hypothesis") or reset:
            states.translation_hypothesis = []
        if not hasattr(states, "translation_input_buffer") or reset:
            states.translation_input_buffer = []

    def _reset_state_for_asr_segment(self, states: AgentStates):
        states.last_transcribed = 0
        states.previous_segment_transcript = getattr(states, "stable_transcript", [])[-self.transcript_context:] if self.transcript_context > 0 else []
        states.stable_transcript = []
        states.transcript_hypothesis = []

    def _transcribe(self, states: AgentStates, segmenter_action: TranslateAction):
        speech_to_translate = segmenter_action.speech_to_translate()
        if len(speech_to_translate) == 0:
            return ""
        speech_to_translate = np.array(speech_to_translate)
        segments, _ = self.whisper_model.transcribe(
            speech_to_translate,
            language=self.whisper_language,
            without_timestamps=True,
            prefix=" ".join(states.stable_transcript),
            initial_prompt=" ".join(states.previous_segment_transcript),
        )
        decoded_output = " ".join([segment.text for segment in segments]).split()
        stable_len = len(states.stable_transcript)
        if not segmenter_action.segment_finished:
            for prev_token, curr_token in zip(states.transcript_hypothesis[stable_len:], decoded_output[stable_len:-1]):
                if prev_token != curr_token:
                    break
                stable_len += 1
        else:
            stable_len = len(decoded_output)
        new_transcription = decoded_output[len(states.stable_transcript):stable_len]
        states.stable_transcript = decoded_output[:stable_len]
        states.last_transcribed = segmenter_action.segment_length()
        states.transcript_hypothesis = decoded_output
        return new_transcription
    
    def _translate(self, states: AgentStates, finish: bool):
        transcript_to_translate = translation_input_buffer = states.translation_input_buffer

        if len(translation_input_buffer) > self.translation_max_input_length_soft and not finish:
            for i, token in enumerate(translation_input_buffer[states.last_translated:], states.last_translated):
                if token.endswith((".", "!", "?")):
                    transcript_to_translate = translation_input_buffer[:i+1]
                    states.translation_input_buffer = translation_input_buffer[i+1:]
                    finish = True
                    break
            if len(transcript_to_translate) > self.translation_max_input_length_hard:
                transcript_to_translate = transcript_to_translate[:self.translation_max_input_length_hard]
                states.translation_input_buffer = translation_input_buffer[self.translation_max_input_length_hard:]
                finish = True

        if len(transcript_to_translate) - self.translation_la_policy >= states.last_translated or finish:   
            source = " ".join(transcript_to_translate)
            prefix = " ".join(states.stable_translation)

            tokens = self.translation_tokenizer(
                source,
                text_target=prefix,
                return_tensors="pt",
            )

            input_ids = tokens.input_ids.to(self.device)
            decoder_input_ids = tokens.labels[:, :-1].to(self.device)

            output = self.translation_model.generate(
                input_ids,
                decoder_input_ids=decoder_input_ids,
            )[0]
            decoded_output = self.translation_tokenizer.decode(output, skip_special_tokens=True).strip().split()
            stable_len = len(states.stable_translation)
            if not finish:
                for prev_token, curr_token in zip(states.translation_hypothesis[stable_len:], decoded_output[stable_len:-1]):
                    if prev_token != curr_token:
                        break
                    stable_len += 1
            else:
                stable_len = len(decoded_output)
            new_translation = decoded_output[len(states.stable_translation):stable_len]
            states.translation_hypothesis = decoded_output if not finish else []
            states.stable_translation = decoded_output[:stable_len] if not finish else []
            states.last_translated = len(transcript_to_translate) if not finish else 0
            return " ".join(new_translation)
        else:
            return ""

    def policy(self, states: Optional[AgentStates] = None):
        if states is None:
            states = self.states
        self._ensure_state_attributes(states)
        
        segmenter_action = self.segmenter.policy(states)

        if isinstance(segmenter_action, TranslateAction):
            if (
                segmenter_action.segment_length() >= states.last_transcribed +
                (self.step_length if not segmenter_action.segment_finished else 0)
            ):
                new_transcription = self._transcribe(states, segmenter_action)
                if len(new_transcription) > 0:
                    states.translation_input_buffer.extend(new_transcription)
                    logging.info(f"Input buffer: {' '.join(states.translation_input_buffer)}")
                

                new_translation = self._translate(states, segmenter_action.source_finished)
                logging.info(f"Translated: {new_translation}")
                logging.info(f"Stable translation: {' '.join(states.stable_translation)}")
                logging.info("")

                if segmenter_action.segment_finished:
                    self._reset_state_for_asr_segment(states)

                if segmenter_action.source_finished:
                    self._ensure_state_attributes(states, reset=True)

                return WriteAction(
                    new_translation,
                    segmenter_action.source_finished,
                )
            else:
                return WriteAction("", False)
        elif isinstance(segmenter_action, ReadAction):
            return segmenter_action # Pass the read action
        else:
            raise ValueError(f"Unknown action type; got {type(segmenter_action)}, expected {TranslateAction} or {ReadAction}")
import logging
from typing import List, Optional

import torch
from iwslt25.speech_segmentation.speech_segmenter import SpeechSegmenter, TranslateAction
from simuleval.agents.states import AgentStates
from simuleval.agents import SpeechToTextAgent
from simuleval.agents.actions import WriteAction, ReadAction

from transformers import AutoProcessor, SeamlessM4Tv2Model

import numpy as np


class SeamlessM4TAgent(SpeechToTextAgent):
    """
    This is an abstract class for a counter agent that counts the number of segments
    in the input speech. The agent will increment the counter every time the segmenter
    finishes a segment. The agent will output the counter as a string every time the
    segmenter finishes a segment.

    This class is meant to be subclassed which should select the segmenter to use. E.g.:

    ```python
        class CounterAgentWithFixedSegmenter(CounterAgent):
            def __init__(self, args):
                super().__init__(args, SpeechSegmenter(args))

            @staticmethod
            def add_args(parser):
                SpeechSegmenter.add_args(parser)
                super().add_args(parser)
    ```
    """

    def __init__(self, args, segmenter: SpeechSegmenter):
        super().__init__(args)
        assert segmenter is not None, "segmenter must be provided"
        self.segmenter = segmenter
        self.segment_counter = 0
        self.step_length = args.step_length
        self.seamless_m4t_model = SeamlessM4Tv2Model.from_pretrained(
            "facebook/seamless-m4t-v2-large")
        self.seamless_m4t_processor = AutoProcessor.from_pretrained(
            "facebook/seamless-m4t-v2-large")
        self.seamless_m4t_vocab = self.seamless_m4t_processor.tokenizer.get_vocab()
        self.tgt_lang = args.seamless_m4t_tgt_lang
        self.device = args.device
        self.seamless_m4t_model = self.seamless_m4t_model.to(self.device)
        self.output_words_valid_words_only = args.eval_latency_unit == "word"

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
            "--seamless-m4t-model",
            choices=["facebook/seamless-m4t-medium",
                     "facebook/seamless-m4t-large", "facebook/seamless-m4t-v2-large"],
            default="facebook/seamless-m4t-v2-large",
        )
        parser.add_argument(
            "--seamless-m4t-tgt-lang",
            type=str,
            default="deu",
        )
        parser.add_argument(
            "--device",
            type=str,
            default="cuda",
        )

    def _ensure_state_attributes(self, states: AgentStates):
        if not hasattr(states, "last_translated"):
            states.last_translated = 0
        if not hasattr(states, "stable_hypothesis"):
            states.stable_hypothesis = []
        if not hasattr(states, "hypothesis"):
            states.hypothesis = []

    def _trim_to_last_word(self, hypothesis: List[int]):
        last_valid = len(hypothesis)
        while last_valid > 0 and self.seamless_m4t_vocab.get(hypothesis[last_valid - 1], "").startswith("▁"):
            logging.info(
                f"Token {hypothesis[last_valid - 1]} ({self.seamless_m4t_vocab.get(hypothesis[last_valid - 1], '')}) is a part of a word")
            last_valid -= 1
        return hypothesis[:last_valid]

    def _local_agreement(self, states: AgentStates, new_hypothesis: List[int], segment_finished: bool):
        curr_len = len(states.stable_hypothesis)
        if not segment_finished:
            stable_len = 0
            for stable_len, (a, b) in enumerate(zip(states.hypothesis, new_hypothesis)):
                if a != b:
                    break
            states.hypothesis = new_hypothesis

            # nothing new
            if stable_len <= curr_len:
                return ""

            if self.output_words_valid_words_only:
                new_stable_hypothesis = self._trim_to_last_word(
                    new_hypothesis[:stable_len]
                )
            else:
                new_stable_hypothesis = new_hypothesis[:stable_len]
        else:
            new_stable_hypothesis = new_hypothesis

        if len(new_stable_hypothesis) > curr_len:
            states.stable_hypothesis = new_stable_hypothesis
            new_tokens = new_stable_hypothesis[curr_len:]
            new_text = self.seamless_m4t_processor.decode(
                new_tokens, skip_special_tokens=True)
            return new_text
        else:
            return ""

    def _translate(self, states: AgentStates, segmenter_action: TranslateAction):
        semgment_or_source_finished = (
            segmenter_action.segment_finished
              or segmenter_action.source_finished
        )

        speech_to_translate = segmenter_action.speech_to_translate()
        if len(speech_to_translate) < 4000:
            return ""

        speech_to_translate = torch.tensor(speech_to_translate).unsqueeze(0)
        audio_inputs = self.seamless_m4t_processor(
            audios=speech_to_translate, return_tensors="pt")
        audio_inputs = {k: v.to(self.device) for k, v in audio_inputs.items()}

        if len(states.stable_hypothesis) > 1:
            audio_inputs["decoder_input_ids"] = torch.tensor(
                states.stable_hypothesis).unsqueeze(0).to(self.device)
        else:
            audio_inputs["tgt_lang"] = self.tgt_lang

        output = self.seamless_m4t_model.generate(
            **audio_inputs, generate_speech=False)[0][0].cpu().numpy()
        logging.info(f"Model output: {output}")

        return self._local_agreement(states, output, semgment_or_source_finished)

    def policy(self, states: Optional[AgentStates] = None):
        if states is None:
            states = self.states
        self._ensure_state_attributes(states)

        segmenter_action = self.segmenter.policy(states)

        if isinstance(segmenter_action, TranslateAction):
            if (
                segmenter_action.segment_length() >= states.last_translated +
                (self.step_length if not segmenter_action.segment_finished else 0)
            ):
                new_transcription = self._translate(states, segmenter_action)
                logging.info(f"translated: {new_transcription}")
                states.last_translated = segmenter_action.segment_length()
                if segmenter_action.segment_finished:
                    states.last_translated = 0
                    states.stable_hypothesis = []
                    states.hypothesis = []
                return WriteAction(
                    new_transcription,
                    segmenter_action.source_finished,
                )
            else:
                return ReadAction()
        elif isinstance(segmenter_action, ReadAction):
            return segmenter_action  # Pass the read action
        else:
            raise ValueError(
                f"Unknown action type; got {type(segmenter_action)}, expected {TranslateAction} or {ReadAction}")

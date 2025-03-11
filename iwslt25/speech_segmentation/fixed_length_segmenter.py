import logging
from typing import Union
from SimulEval.simuleval.agents.actions import ReadAction
from SimulEval.simuleval.agents.states import AgentStates
from ..speech_segmentation.speech_segmenter import SpeechSegmenter, TranslateAction


class FixedLengthSegmenter(SpeechSegmenter):
    '''
    Segmenter that segments the speech into fixed length segments
    '''

    def __init__(self, args):
        self.segment_length = args.segment_length
        assert self.segment_length > 0

    @staticmethod
    def add_args(parser):
        parser.add_argument("--segment-length", default=10.0,
                            type=float, help="Segment length in seconds")

    def policy(self, states: AgentStates) -> Union[TranslateAction, ReadAction]:
        assert states is not None

        if not hasattr(states, "last_segment_position"):
            states.last_segment_position = 0

        if states.source_sample_rate == 0:
            # empty source, source_sample_rate not set yet
            length_in_seconds = 0.
        else:
            length_in_seconds = (
                len(states.source) - states.last_segment_position) / states.source_sample_rate

        segment_finished = (
            length_in_seconds >= self.segment_length
            or states.source_finished
        )
        segment_start = states.last_segment_position
        segment_end = min(
            segment_start + int(self.segment_length *
                                states.source_sample_rate),
            len(states.source),
        )

        if states.source_finished:
            states.last_segment_position = 0
        elif segment_finished:
            states.last_segment_position = segment_end

        logging.info(
            f"Current from {segment_start / states.source_sample_rate} to {segment_end / states.source_sample_rate} seconds; source length: {len(states.source) / states.source_sample_rate}; segment finished: {segment_finished}"
        )

        return TranslateAction(
            states=states,
            speech_to_translate_start=segment_start,
            speech_to_translate_end=segment_end,
            segment_finished=segment_finished,
            source_finished=states.source_finished,
        )

from typing import Optional, Union
from simuleval.agents.states import AgentStates
from simuleval.agents.actions import Action, ReadAction


class TranslateAction(Action):
    """
    Action to return when SpeechSegmenter decides to generate a translation
    """

    states: AgentStates
    speech_to_translate_start: int
    speech_to_translate_end: int
    segment_finished: bool

    def __init__(
        self,
        states: AgentStates,
        speech_to_translate_start: int,
        speech_to_translate_end: int,
        segment_finished: bool,
        source_finished: bool,
    ):
        assert states is not None
        assert (
            0
            <= speech_to_translate_start
            <= speech_to_translate_end
            <= len(states.source)
        ), f"Invalid indices: {speech_to_translate_start}, {speech_to_translate_end}, {len(states.source)}"
        self.states = states
        self.speech_to_translate_start = speech_to_translate_start
        self.speech_to_translate_end = speech_to_translate_end
        self.segment_finished = segment_finished
        self.source_finished = source_finished

    def speech_to_translate(self):
        """
        Return the speech to translate.
        You can also access the source speech using self.states.source using TranscribeAction.speech_to_translate_start
        and TranscribeAction.speech_to_translate_end as indices. This might be useful if your model can utilize previous context.
        """
        return self.states.source[
            self.speech_to_translate_start : self.speech_to_translate_end
        ]

    def segment_length(self):
        """
        Return the length of the segment in seconds
        """
        return (
            self.speech_to_translate_end - self.speech_to_translate_start
        ) / self.states.source_sample_rate

    def segment_end(self):
        """
        Return the end of the segment in seconds
        """
        return self.speech_to_translate_end / self.states.source_sample_rate
    
    def segment_start(self):
        """
        Return the start of the segment in seconds
        """
        return self.speech_to_translate_start / self.states.source_sample_rate

class SpeechSegmenter(object):
    """
    Base class for speech segmenters
    """

    @staticmethod
    def add_args(parser):
        """
        Add arguments to the parser
        """
        pass

    def policy(self, states: AgentStates) -> Union[TranslateAction, ReadAction]:
        """ """
        raise NotImplementedError("This method should be implemented in the subclass")

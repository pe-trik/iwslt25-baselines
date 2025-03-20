from simuleval.utils import entrypoint
from iwslt25.speech_segmentation.fixed_length_segmenter import FixedLengthSegmenter
from iwslt25.agents.cascade_agent import CascadeAgent


@entrypoint
class CascadeAgentWitFixedLengthSegmenter(CascadeAgent):
    """
    WhisperAgent that uses FixedLengthSegmenter to segment the speech
    """
    def __init__(self, args):
        super().__init__(args, FixedLengthSegmenter(args))

    @staticmethod
    def add_args(parser):
        """
        Add arguments to the parser
        """
        FixedLengthSegmenter.add_args(parser)
        CascadeAgent.add_args(parser)
from simuleval.utils import entrypoint
from iwslt25.speech_segmentation.fixed_length_segmenter import FixedLengthSegmenter
from iwslt25.agents.seamless_m4t_agent import SeamlessM4TAgent


@entrypoint
class SeamlessM4TAgentWithFixedSegmenter(SeamlessM4TAgent):
    """
    SeamlessM4TAgent that uses FixedSegmenter to segment the speech
    """
    def __init__(self, args):
        super().__init__(args, FixedLengthSegmenter(args))

    @staticmethod
    def add_args(parser):
        """
        Add arguments to the parser
        """
        FixedLengthSegmenter.add_args(parser)
        SeamlessM4TAgent.add_args(parser)
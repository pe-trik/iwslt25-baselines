from simuleval.utils import entrypoint
from iwslt25.speech_segmentation.vad_segmenter import VADSegmenter
from iwslt25.agents.seamless_m4t_agent import SeamlessM4TAgent


@entrypoint
class WhisperAgentWithFixedSegmenter(SeamlessM4TAgent):
    """
    WhisperAgent that uses VADSegmenter to segment the speech
    """
    def __init__(self, args):
        super().__init__(args, VADSegmenter(args))

    @staticmethod
    def add_args(parser):
        """
        Add arguments to the parser
        """
        VADSegmenter.add_args(parser)
        SeamlessM4TAgent.add_args(parser)
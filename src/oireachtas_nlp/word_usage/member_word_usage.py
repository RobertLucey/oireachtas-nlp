import tqdm

from oireachtas_nlp.utils import get_speaker_para_map
from oireachtas_nlp import logger
from oireachtas_nlp.word_usage.base_word_usage import BaseWordUsage


class MemberWordUsage(BaseWordUsage):

    def process(self):
        logger.info("Getting words")
        speaker_map = get_speaker_para_map()

        logger.info("Processing words")
        for speaker, paras in tqdm.tqdm(speaker_map.items()):
            self.update_groups([speaker], paras)

        logger.info("Logging stats")
        self.log_stats()

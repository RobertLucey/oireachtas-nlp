import tqdm

from oireachtas_nlp.utils import get_party_para_map
from oireachtas_nlp import logger
from oireachtas_nlp.word_usage.base_word_usage import BaseWordUsage


class PartyWordUsage(BaseWordUsage):

    def process(self):
        logger.info("Getting words")
        party_map = get_party_para_map()

        logger.info("Processing words")
        for party, paras in tqdm.tqdm(party_map.items()):
            self.update_groups([party], paras)

        logger.info("Logging stats")
        self.log_stats()

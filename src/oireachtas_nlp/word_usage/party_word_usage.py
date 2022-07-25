from collections import defaultdict

import tqdm

from oireachtas_data import members
from oireachtas_data.utils import iter_debates

from oireachtas_nlp import logger
from oireachtas_nlp.word_usage.base_word_usage import BaseWordUsage


class PartyWordUsage(BaseWordUsage):
    def process(self):
        party_map = defaultdict(list)
        logger.info("Getting words")
        for debate in tqdm.tqdm(iter_debates()):
            for speaker, paras in debate.content_by_speaker.items():
                parties = members.parties_of_member(speaker)
                if parties is None:
                    continue
                for party in parties:
                    party_map[party].extend(paras)

        logger.info("Processing words")
        for party, paras in tqdm.tqdm(party_map.items()):
            self.update_groups([party], paras)

        logger.info("Logging stats")
        self.log_stats()

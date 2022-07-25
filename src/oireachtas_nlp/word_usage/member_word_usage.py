from collections import defaultdict

import tqdm

from oireachtas_data.utils import iter_debates

from oireachtas_nlp import logger
from oireachtas_nlp.word_usage.base_word_usage import BaseWordUsage


class MemberWordUsage(BaseWordUsage):
    def process(self):
        speaker_map = defaultdict(list)
        logger.info("Getting words")
        for debate in tqdm.tqdm(iter_debates()):
            for speaker, paras in debate.content_by_speaker.items():
                speaker_map[speaker].extend(paras)

        logger.info("Processing words")
        for speaker, paras in tqdm.tqdm(speaker_map.items()):
            self.update_groups([speaker], paras)

        logger.info("Logging stats")
        self.log_stats()

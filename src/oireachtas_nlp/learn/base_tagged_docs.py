from random import shuffle
from collections import defaultdict

import tqdm

from gensim.models.doc2vec import TaggedDocument

from oireachtas_data import members
from oireachtas_data.utils import iter_debates

from oireachtas_nlp import logger
from oireachtas_nlp.models.text import TextBody
from oireachtas_nlp.utils import flatten


class BaseTaggedDocs(object):
    def __init__(
        self,
        min_per_group=10,
        max_per_group=100,
        exclude_para_hashes=None,
        min_content_len=5000,
    ):
        """

        :kwarg min_per_group: The minimum required items for the
            entire tag / group to be processed
        """
        self.items = []
        self.docs = []
        self.counter = defaultdict(int)
        self.min_per_group = min_per_group
        self.max_per_group = max_per_group
        self.loaded_tagged_docs = False
        self.exclude_para_hashes = (
            exclude_para_hashes if exclude_para_hashes is not None else set()
        )
        self.min_content_len = min_content_len

    def get_para_hashes(self):
        hashes = []
        for speaker, paras in self.items:
            hashes.extend([p.content_hash for p in paras])
        return set(hashes)

    def load(self, speaker, content):
        if self.should_include(speaker):
            self.items.append((speaker, content))

    def load_tagged_docs(self) -> None:
        if self.loaded_tagged_docs:
            return

        logger.info(f'Loading "{self.NAME}" tagged docs')
        for debate in tqdm.tqdm(iter_debates()):

            for speaker, paras in debate.content_by_speaker.items():

                # TODO: map speakers to the pid "Bruce Wayne" -> "#BruceWayne"

                # If we don't recognise the speaker then ignore
                member = members.get_member_from_name(speaker)
                if member is None:
                    continue

                if speaker == "#":
                    continue
                if "Comhairle" in speaker:
                    continue
                if "Cathaoirleach" in speaker:
                    continue
                if "Taoiseach" in speaker:
                    continue

                content_str = "\n\n".join(
                    [
                        p.content
                        for p in paras
                        if p.content_hash not in self.exclude_para_hashes
                    ]
                )

                if len(content_str) < self.min_content_len:
                    continue

                self.load(speaker, paras)

        self.loaded_tagged_docs = True

        logger.info(f'Finished loading "{self.NAME}" tagged docs')

    def should_include(self, item):
        raise NotImplementedError()

    def get_group_name(self, item):
        raise NotImplementedError()

    def __iter__(self):
        for speaker, paras in self.items:

            body = TextBody(content="\n\n".join([p.content for p in paras]))
            yield TaggedDocument(
                body.content.split(), [str(speaker + "_%s") % (self.counter[speaker])]
            )
            self.counter[speaker] += 1

    def to_array(self):
        self.docs = [i for i in self]
        return self.docs

    def perm(self):
        shuffle(self.docs)
        return self.docs

    def clean_data(self) -> None:
        logger.info(f'Cleaning "{self.NAME}" data')

        logger.info("Start removing groups with too little content")
        groups_count = defaultdict(int)
        for item in self.items:
            if self.get_group_name(item) is not None:
                groups_count[self.get_group_name(item)] += 1
        self.items = [
            item
            for item in self.items
            if groups_count[self.get_group_name(item)] >= self.min_per_group
        ]
        logger.info("Finished removing groups with too little content")

        logger.info("Start limiting the number of items per group")
        group_items_map = defaultdict(list)
        for item in self.items:
            group_items_map[self.get_group_name(item)].append(item)
        self.items = flatten(
            [v[0 : self.max_per_group] for k, v in group_items_map.items()]
        )
        logger.info("Finished limiting the number of items per group")

        logger.info(f'Finished cleaning "{self.NAME}" data')

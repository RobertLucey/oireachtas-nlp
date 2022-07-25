from collections import defaultdict

from gensim.models.doc2vec import TaggedDocument

from oireachtas_data import members

from oireachtas_nlp import logger
from oireachtas_nlp.utils import flatten
from oireachtas_nlp.models.text import TextBody
from oireachtas_nlp.learn.base_tagged_docs import BaseTaggedDocs


class MemberTaggedDocs(BaseTaggedDocs):

    NAME = "member"

    def __iter__(self):
        for speaker, paras in self.items:

            if "%" in speaker:
                continue

            if speaker.strip() == "#":
                continue

            body = TextBody(content="\n\n".join([p.content for p in paras]))
            yield TaggedDocument(
                body.content.split(), [str(speaker + "_%s") % (self.counter[speaker])]
            )
            self.counter[speaker] += 1

    def get_group_name(self, item) -> int:
        return item[0]

    def should_include(self, debate):
        return True

    def load(self, speaker, content):
        if self.should_include(speaker):
            self.items.append((speaker, content))


class PartyTaggedDocs(BaseTaggedDocs):

    NAME = "party"

    def __iter__(self):
        for party, paras in self.items:

            if party is None:
                continue

            body = TextBody(content="\n\n".join([p.content for p in paras]))
            yield TaggedDocument(
                body.content.split(), [str(party + "_%s") % (self.counter[party])]
            )
            self.counter[party] += 1

    def get_group_name(self, item):
        parties = members.parties_of_member(item)
        if parties:
            return parties[0].replace("_", "")

    def should_include(self, debate):
        return True

    def load(self, speaker, content):
        if self.should_include(speaker):
            party = self.get_group_name(speaker)

            if party is None:
                return

            # Independant is a bit risky to include
            # should make this an option
            if party == "Independent":
                return

            self.items.append((party, content))

    def clean_data(self) -> None:

        logger.info("Cleaning data")

        logger.info("Start removing groups with too little content")
        groups_count = defaultdict(int)
        for item in self.items:
            if item is not None:
                groups_count[item[0]] += 1
        self.items = [
            item for item in self.items if groups_count[item[0]] >= self.min_per_group
        ]
        logger.info("Finished removing groups with too little content")

        logger.info("Start limiting the number of items per group")
        group_items_map = defaultdict(list)
        for item in self.items:
            group_items_map[item[0]].append(item)
        self.items = flatten(
            [v[0 : self.max_per_group] for k, v in group_items_map.items()]
        )
        logger.info("Finished limiting the number of items per group")

        logger.info("Finished cleaning data")

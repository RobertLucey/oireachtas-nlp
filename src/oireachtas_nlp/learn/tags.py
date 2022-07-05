from collections import defaultdict

from gensim.models.doc2vec import TaggedDocument

from oireachtas_data import members

from oireachtas_nlp.utils import flatten
from oireachtas_nlp.models.text import TextBody
from oireachtas_nlp.learn.base_tagged_docs import BaseTaggedDocs


class MemberTaggedDocs(BaseTaggedDocs):

    def __iter__(self):
        for speaker, paras in self.items:

            if '%' in speaker:
                continue

            if speaker.strip() == '#':
                continue

            body = TextBody(content='\n\n'.join(
                [p.content for p in paras]
            ))
            yield TaggedDocument(
                self.content_cleaner(body).split(),
                [str(speaker + '_%s') % (self.counter[speaker])]
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

    def __iter__(self):
        for speaker, paras in self.items:
            party = speaker

            if party is None:
                continue

            body = TextBody(content='\n\n'.join(
                [p.content for p in paras]
            ))
            yield TaggedDocument(
                self.content_cleaner(body).split(),
                [str(party + '_%s') % (self.counter[party])]
            )
            self.counter[party] += 1

    def get_group_name(self, item):
        parties = members.parties_of_member(item)
        if parties:
            return parties[0].replace('_', '')

    def should_include(self, debate):
        return True

    def load(self, speaker, content):
        if self.should_include(speaker):
            party = self.get_group_name(speaker)

            if party is None:
                return

            # Independant is a bit risky to include
            # should make this an option
            if party == 'Independent':
                return

            self.items.append((party, content))

    def clean_data(self) -> None:

        def cull() -> None:
            groups_count = defaultdict(int)

            for item in self.items:
                if item is not None:
                    groups_count[item[0]] += 1

            self.items = [
                item for item in self.items if groups_count[item[0]] >= self.min_per_group
            ]

            groups_count = defaultdict(int)
            for item in self.items:
                if item[0] is not None:
                    groups_count[item[0]] += 1

            group_items_map = defaultdict(list)
            for item in self.items:
                group_items_map[item[0]].append(item)
            self.items = flatten([v[0:self.min_per_group] for k, v in group_items_map.items()])

        print('Cleaning data')

        cull()

        group_counts = defaultdict(int)
        for item in self.items:
            if item[0] is not None:
                group_counts[item[0]] += 1

        cleaned_items = []
        for name, count in group_counts.items():
            group_count = 0
            for item in self.items:
                if item[0] == name:
                    if group_count < self.min_per_group:
                        cleaned_items.append(item)
                        group_count += 1

        self.items = cleaned_items

        group_counts = defaultdict(int)
        for item in self.items:
            if item[0] is not None:
                group_counts[item[0]] += 1

        print('Finished cleaning data')

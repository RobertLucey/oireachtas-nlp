from random import shuffle
from collections import defaultdict

from gensim.models.doc2vec import TaggedDocument

from oireachtas_nlp.utils import flatten


class BaseTaggedDocs(object):

    def __init__(self, min_per_group=10):
        """

        :kwarg min_per_group: The minimum required items for the
            entire tag / group to be processed
        """
        self.items = []
        self.docs = []
        self.num_items = 0
        self.counter = defaultdict(int)
        self.min_per_group = min_per_group

    def load(self, speaker, content):
        if self.should_include(speaker):
            self.items.append((speaker, content))
            self.num_items += 1

    def should_include(self, item):
        raise NotImplementedError()

    def get_group_name(self, item):
        raise NotImplementedError()

    def __iter__(self):
        for item in self.items:
            group = self.get_group_name(item)
            yield TaggedDocument(
                self.content_cleaner(item).split(),
                [str(group + '_%s') % (self.counter[group])]
            )
            self.counter[group] += 1

    def to_array(self):
        self.docs = [i for i in self]
        return self.docs

    def perm(self):
        shuffle(self.docs)
        return self.docs

    def content_cleaner(self, item) -> str:
        return item.content

    def clean_data(self) -> None:

        def cull() -> None:
            groups_count = defaultdict(int)
            for item in self.items:
                if self.get_group_name(item) is not None:
                    groups_count[self.get_group_name(item)] += 1

            self.items = [
                item for item in self.items if groups_count[self.get_group_name(item)] >= self.min_per_group
            ]

            groups_count = defaultdict(int)
            for item in self.items:
                if self.get_group_name(item) is not None:
                    groups_count[self.get_group_name(item)] += 1

            group_items_map = defaultdict(list)
            for item in self.items:
                group_items_map[self.get_group_name(item)].append(item)
            self.items = flatten([v[0:self.min_per_group] for k, v in group_items_map.items()])

        print('Cleaning data')

        cull()

        group_counts = defaultdict(int)
        for item in self.items:
            if self.get_group_name(item) is not None:
                group_counts[self.get_group_name(item)] += 1

        cleaned_items = []
        for name, count in group_counts.items():
            group_count = 0
            for item in self.items:
                if self.get_group_name(item) == name:
                    if group_count < self.min_per_group:
                        cleaned_items.append(item)
                        group_count += 1

        self.items = cleaned_items

        group_counts = defaultdict(int)
        for item in self.items:
            if self.get_group_name(item) is not None:
                group_counts[self.get_group_name(item)] += 1

        print('Finished cleaning data')

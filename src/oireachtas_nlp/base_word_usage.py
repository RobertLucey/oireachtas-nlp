from collections import defaultdict

from oireachtas_data import members
from oireachtas_data.utils import iter_debates

from oireachtas_nlp.models.para import ExtendedParas


class BaseWordUsage:

    def __init__(
        self,
        only_words=None,
        only_groups=None,
        head_tail_len=10,
        log_rate=100,
    ):
        """

        :kwarg only_words: Only include these words as interesting
        :kwarg only_groups: Only include data of groups in this list
        :kwarg head_tail_len: How many words to give back for each comparison
        :kwarg log_rate: After how many debates processed to log the stats
        """
        self.only_words = only_words
        self.only_groups = only_groups
        self.head_tail_len = head_tail_len
        self.log_rate = log_rate
        self.groups = defaultdict(lambda: defaultdict(int))
        self.global_words = set()

    def grouper(self, debate):
        raise NotImplementedError()

    def update_groups(self, speaker, paras):
        """
        Given a speaker and their paragraphs update the groups
        associated with that speaker

        :param speaker: str
        :param paras: oireachtas_nlp.models.para.Paras
        """

        paras = ExtendedParas(data=paras)

        group_names = set(self.grouper(speaker))
        if self.only_groups is not None:
            group_names = group_names.intersection(set(self.only_groups))
        if group_names == set():
            return

        counts = paras.text_obj.get_word_counts()
        local_words = counts.keys()

        for missing_word in self.global_words - set(list(local_words)):
            counts[missing_word] = 0

        self.global_words.union(counts.keys())

        for group_name in group_names:
            for word, count in counts.items():
                self.groups[group_name][word] += count

    def log_stats(self):
        perc_groups = defaultdict(lambda: defaultdict(int))

        for group_name in self.groups.keys():
            group_count = sum(list(self.groups[group_name].values()))
            for word, count in self.groups[group_name].items():
                if self.only_words and word not in self.only_words:
                    continue
                perc = (count / group_count) * 100
                perc_groups[group_name][word] = perc

        results = []
        for base_group in perc_groups.keys():
            if base_group is None:
                continue
            base_keys = list(perc_groups[base_group].keys())
            for cmp_group in perc_groups.keys():
                if cmp_group is None or cmp_group == base_group:
                    continue

                words_data = {}
                for word in base_keys + list(perc_groups[cmp_group].keys()):
                    words_data[word] = perc_groups[base_group].get(word, 0) - perc_groups[cmp_group].get(word, 0)

                data = [
                    (i[0], round(i[1], 2)) for i in sorted(
                        words_data.items(),
                        key=lambda item: item[1],
                        reverse=True
                    )[:self.head_tail_len]
                ]

                results.append(
                    (
                        cmp_group,
                        base_group,
                        data
                    )
                )

        for cmp_group, base_group, data in results:
            print(
                '%s > %s: %s' % (
                    base_group,
                    cmp_group,
                    data
                )
            )

    def process(self):
        for idx, debate in enumerate(iter_debates()):
            for speaker, paras in debate.content_by_speaker.items():
                self.update_groups(speaker, paras)
            if idx % self.log_rate == 0 and self.log_rate != 0:
                self.log_stats()


class MemberWordUsage(BaseWordUsage):

    def grouper(self, member):
        if self.only_groups is not None:
            if member not in self.only_groups:
                return []
        return [member]


class PartyWordUsage(BaseWordUsage):

    def grouper(self, member):
        parties = members.parties_of_member(member)
        if parties is None:
            return []
        return parties


class GenderWordUsage(BaseWordUsage):

    def grouper(self, member):
        raise NotImplementedError()

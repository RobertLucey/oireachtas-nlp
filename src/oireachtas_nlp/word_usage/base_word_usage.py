from collections import defaultdict

from oireachtas_nlp import logger
from oireachtas_nlp.models.para import ExtendedParas


class BaseWordUsage:

    def __init__(
        self,
        only_words=None,
        only_groups=None,
        head_tail_len=5,
        min_paras_per_group=10
    ):
        """

        :kwarg only_words: Only include these words as interesting
        :kwarg only_groups: Only include data of groups in this list
        :kwarg head_tail_len: How many words to give back for each comparison
        """
        self.only_words = only_words
        self.only_groups = only_groups
        self.head_tail_len = head_tail_len
        self.min_paras_per_group = min_paras_per_group

        self.groups = defaultdict(lambda: defaultdict(int))
        self.global_words = set()

    def update_groups(self, group_names, paras):
        """
        Given a speaker and their paragraphs update the groups
        associated with that speaker

        :param speaker: str
        :param paras: oireachtas_nlp.models.para.Paras
        """

        if len(paras) < self.min_paras_per_group:
            return

        paras = ExtendedParas(data=paras)

        if self.only_groups is not None:
            group_names = group_names.intersection(self.only_groups)
        if group_names == set():
            return

        counts = paras.text_obj.get_word_counts()
        local_words = counts.keys()

        for missing_word in self.global_words - set(local_words):
            counts[missing_word] = 0

        self.global_words.update(counts.keys())

        counts_items = counts.items()
        for group_name in group_names:
            for word, count in counts_items:
                self.groups[group_name][word] += count

    def log_stats(self):
        perc_groups = defaultdict(lambda: defaultdict(int))

        logger.info('Setting group words stats')
        for group_name in self.groups.keys():
            group_count = sum(self.groups[group_name].values())
            for word, count in self.groups[group_name].items():
                if self.only_words and word not in self.only_words:
                    continue
                perc = (count / group_count) * 100
                perc_groups[group_name][word] = perc

        base_cmp_results = defaultdict(dict)
        logger.info('Calculating differences')
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

                base_cmp_results[base_group][cmp_group] = data
                logger.info(
                    '%s > %s: %s' % (
                        base_group,
                        cmp_group,
                        data
                    )
                )

        return base_cmp_results

    def process(self):
        raise NotImplementedError()

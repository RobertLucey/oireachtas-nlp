from unittest import TestCase

from oireachtas_data.models.para import Para

from oireachtas_nlp.word_usage.base_word_usage import BaseWordUsage


class BaseWordUsageTest(TestCase):

    def test_update_groups(self):
        word_usage = BaseWordUsage(min_paras_per_group=0)

        para1 = Para(
            title='title 1',
            eid=None,
            content='content of title 1'
        )

        para2 = Para(
            title='title 2',
            eid=None,
            content='explosion of title 2'
        )

        para3 = Para(
            title='title 2',
            eid=None,
            content='blackjack the horse 3'
        )

        word_usage.update_groups(['group1', 'group2'], [para1, para2])
        word_usage.update_groups(['group1'], [para3])

        self.assertEqual(
            word_usage.global_words,
            {'content', 'title', 'horse', 'blackjack', 'explosion'}
        )
        self.assertEqual(
            {k: dict(v) for k, v in dict(word_usage.groups).items()},
            {'group1': {'content': 1, 'title': 2, 'explosion': 1, 'blackjack': 1, 'horse': 1}, 'group2': {'content': 1, 'title': 2, 'explosion': 1}}
        )

from unittest import TestCase

from oireachtas_data.models.para import Para

from oireachtas_nlp.word_usage.base_word_usage import BaseWordUsage


class BaseWordUsageTest(TestCase):
    def test_update_groups(self):
        word_usage = BaseWordUsage(min_paras_per_group=0)

        para1 = Para(title="title 1", eid=None, content="content of title 1")

        para2 = Para(title="title 2", eid=None, content="explosion of title 2")

        para3 = Para(title="title 2", eid=None, content="blackjack the horse 3")

        word_usage.update_groups(["group1", "group2"], [para1, para2])
        word_usage.update_groups(["group1"], [para3])

        self.assertEqual(
            word_usage.global_words,
            {"content", "title", "horse", "blackjack", "explosion"},
        )
        self.assertEqual(
            {k: dict(v) for k, v in dict(word_usage.groups).items()},
            {
                "group1": {
                    "content": 1,
                    "title": 2,
                    "explosion": 1,
                    "blackjack": 1,
                    "horse": 1,
                },
                "group2": {"content": 1, "title": 2, "explosion": 1},
            },
        )

    def test_update_groups_only_groups_none(self):
        word_usage = BaseWordUsage(min_paras_per_group=0, only_groups=set())

        para1 = Para(title="title 1", eid=None, content="content of title 1")
        word_usage.update_groups(set(["group1"]), [para1])

        self.assertEqual(word_usage.global_words, set())
        self.assertEqual({k: dict(v) for k, v in dict(word_usage.groups).items()}, {})

    def test_update_groups_min_paras_per_group(self):
        word_usage = BaseWordUsage(min_paras_per_group=2)

        para1 = Para(title="title 1", eid=None, content="content of title 1")

        para2 = Para(title="title 2", eid=None, content="explosion of title 2")

        word_usage.update_groups(set(["group1"]), [para1])

        self.assertEqual(word_usage.global_words, set())

        word_usage.update_groups(set(["group1"]), [para1, para2])

        self.assertEqual(word_usage.global_words, {"content", "title", "explosion"})

    def test_all_except(self):
        word_usage = BaseWordUsage(min_paras_per_group=1, head_tail_len=100)

        para1 = Para(title="title 1", eid=None, content="one two three four five")

        para2 = Para(title="title 2", eid=None, content="four five six seven eight")

        word_usage.update_groups(set(["group1"]), [para1])
        word_usage.update_groups(set(["group2"]), [para2])

        word_usage_stats = word_usage.log_stats()

        import pprint

        self.assertEqual(
            dict(word_usage_stats["group1"]["all_except_group1"])["one"], 20
        )
        self.assertEqual(
            dict(word_usage_stats["group1"]["all_except_group1"])["two"], 20
        )
        self.assertEqual(
            dict(word_usage_stats["group1"]["all_except_group1"])["three"], 20
        )
        self.assertEqual(
            dict(word_usage_stats["group1"]["all_except_group1"])["four"], 0
        )
        self.assertEqual(
            dict(word_usage_stats["group1"]["all_except_group1"])["five"], 0
        )
        self.assertEqual(
            dict(word_usage_stats["group1"]["all_except_group1"])["six"], -20
        )
        self.assertEqual(
            dict(word_usage_stats["group1"]["all_except_group1"])["seven"], -20
        )
        self.assertEqual(
            dict(word_usage_stats["group1"]["all_except_group1"])["eight"], -20
        )

        self.assertEqual(
            dict(word_usage_stats["group2"]["all_except_group2"])["one"], -20
        )
        self.assertEqual(
            dict(word_usage_stats["group2"]["all_except_group2"])["two"], -20
        )
        self.assertEqual(
            dict(word_usage_stats["group2"]["all_except_group2"])["three"], -20
        )
        self.assertEqual(
            dict(word_usage_stats["group2"]["all_except_group2"])["four"], 0
        )
        self.assertEqual(
            dict(word_usage_stats["group2"]["all_except_group2"])["five"], 0
        )
        self.assertEqual(
            dict(word_usage_stats["group2"]["all_except_group2"])["six"], 20
        )
        self.assertEqual(
            dict(word_usage_stats["group2"]["all_except_group2"])["seven"], 20
        )
        self.assertEqual(
            dict(word_usage_stats["group2"]["all_except_group2"])["eight"], 20
        )

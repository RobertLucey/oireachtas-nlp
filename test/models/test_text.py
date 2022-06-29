from unittest import TestCase

from oireachtas_nlp.models.text import TextBody


class UtilsTest(TestCase):

    def test_get_word_counts(self):
        self.assertEqual(
            TextBody(
                content='rainbow frog rainbow'
            ).get_word_counts(),
            {'frog': 1, 'rainbow': 2}
        )

        self.assertEqual(
            TextBody(
                content='rainbow frog rainbow moo moo'
            ).get_word_counts(only_include_words=['frog', 'water', 'moo']),
            {'frog': 1, 'moo': 2}
        )

    def test_basic_words(self):
        self.assertEqual(
            TextBody(
                content='rainbow frog rainbow moo moo'
            ).basic_words,
            ['rainbow', 'frog', 'rainbow', 'moo', 'moo']
        )

    def test_words(self):
        self.assertEqual(
            TextBody(
                content='rainbow frog rainbow moo moo'
            ).words,
            ['rainbow', 'frog', 'rainbow', 'moo', 'moo']
        )

    def test_lexical_diversity(self):
        self.assertEqual(
            TextBody(
                content='yes no maybe'
            ).get_lexical_diversity(),
            1
        )

        self.assertEqual(
            TextBody(
                content='no no no'
            ).get_lexical_diversity(),
            1/3.
        )

        self.assertEqual(
            TextBody(
                content='yes yes no no'
            ).get_lexical_diversity(),
            1/2.
        )

    def test_sentences(self):
        self.assertEqual(
            TextBody(
                content='This is the first sentence. This is the second one'
            ).sentences,
            [
                'This is the first sentence.',
                'This is the second one'
            ]
        )

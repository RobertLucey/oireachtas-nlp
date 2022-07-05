from collections import Counter

from cached_property import cached_property

import nltk

from oireachtas_nlp.constants import (
    BORING_WORDS,
    ENG_WORDS,
    EXTENDED_PUNCTUATION
)


class TextBody():

    def __init__(self, *args, **kwargs):
        """

        :kwarg content: Text content as a string
        :kwarg content_path: Path to a txt file containing the content
        """
        self.content = kwargs.get('content', None)
        self.content_path = kwargs.get('content_path', None)

    def get_lexical_diversity(self, only_dictionary_words=False):
        if only_dictionary_words:
            return float(len(set(self.dictionary_words))) / len(self.dictionary_words)
        return float(len(set(self.words))) / self.word_count

    @property
    def basic_words(self):
        return [i for i in self.content.split() if i]

    @property
    def words(self):
        txt = self.content.translate(
            str.maketrans(
                '',
                '',
                ''.join(['\n', '\n\n'] + EXTENDED_PUNCTUATION)
            )
        )
        return [i for i in txt.split() if i]

    @cached_property
    def sentences(self):
        return nltk.sent_tokenize(self.content)

    @cached_property
    def dictionary_words(self):
        return [
            word for word in self.words if word.lower() in ENG_WORDS and word.isalpha()
        ]

    @property
    def word_count(self):
        """

        :return: the number of individual words in the piece of text
        """
        return len(self.basic_words)

    def get_word_counts(self, only_include_words=None):
        """
        Get the counts of dictionary words.

        Usage:
            >>> TextBody(content='Wake me up before you go go!').word_counts()
            {'wake': 1, 'me': 1, 'up': 1, 'before': 1, 'you': 1, 'go': 2}

            >>> TextBody(content='Wake me up before you go go!').word_counts(only_include_words={'up', 'go'})
            {'up': 1, 'go': 2}
        """

        if only_include_words is not None:
            return dict(
                Counter(
                    [
                        w.lower() for w in self.dictionary_words if w.lower() in only_include_words
                    ]
                )
            )

        return dict(
            Counter(
                [
                    w.lower() for w in self.words if all([
                        w.lower() not in BORING_WORDS,
                        w.isalpha()
                    ])
                ]
            )
        )
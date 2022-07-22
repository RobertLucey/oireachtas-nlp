import string
import os

import nltk
from nltk.corpus import stopwords

try:
    nltk.data.find('corpora/words')
except LookupError:  # pragma: nocover
    nltk.download('words')
finally:
    ENG_WORDS = set(nltk.corpus.words.words())

APOSTROPHES = {'’', '\''}
SENTENCE_TERMINATORS = {'.', '?', '!'}
SPEECH_QUOTES = {'`', '‘', '"', '``', '”', '“', '’'}
EXTENDED_PUNCTUATION = list(string.punctuation) + list(SPEECH_QUOTES)

BORING_WORDS = set(stopwords.words('english'))

LOG_LOCATION = '/var/log/oireachtas_nlp/oireachtas_nlp.log' if os.getenv('TEST_ENV', 'False') == 'False' else '/tmp/test_oireachtas_nlp.log'

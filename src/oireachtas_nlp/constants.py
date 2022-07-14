import string
import os

import nltk

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

BORING_WORDS = {'has', 'other', 'well', 'got', 'should', 'away', 'need', 'tell', 'here', 'cannot', 'never', 'now', 'just', 'through', 'think', 'too', 'see', 'want', 'much', 'still', 'head', 'hand', 'after', 'even', 'get', 'only', 'where', 'why', 'their', 'can', 'because', 'right', 'way', 'around', 'my', 'who', 'go', 'said', 'down', 'your', 'than', 'how', 'more', 'enough', 'going', 'off', 'then', 'before', 'over', 'by', 'time', 'or', 'am', 'them', 'an', 'there', 'this', 'will', 'know', 'one', 'me', 'like', 'back', 'when', 'into', 'been', 'so', 'about', 'were', 'are', 'from', 'no', 'we', 'did', 'all', 'him', 'if', 'up', 'what', 'do', 'could', 'be', 'would', 'at', 'but', 'out', 'dom', 'they', 'with', 'have', 'for', 'is', 'as', 'on', 'his', 'that', 'in', 'had', 'was', 'he', 'i', 'it', 'you', 'her', 'she', 'not', 'of', 'a', 'and', 'to', 'the', 'which', 'any', 'some', 'those', 'being', 'made', 'went', 'few', 'our', 'find', 'since', 'gone', 'came', 'again', 'us', 'own', 'may', 'its', 'such', 'both', 'ar', 'every', 'example', 'might', 'very', 'same', 'change', 'does', 'themselves', 'under', 'else', 'say', 'met', 'let', 'knew', 'ever', 'p', 'thou', 'come', 'put', 'thought', 'knew', 'make', 'give', 'once', 'felt', 'looking', 'always', 'behind', 'something', 'anyone', 'side', 'seen', 'm', 't', 'g', 'b', 'each', 'upon', 'another', 'really', 'these', 'though', 'above', 'told', 'c', 'y', 'en', 'el', 'also', 'de', 'la', 'un', 'las', 'many', 'most', 'se', 'lo', 'es', 'thing', 're', 'against', 'later', 'pol', 'wis', 'ae', 'esca', 'amma', 'soka', 'onto', 'toward', 'turned', 'perhaps', 'first', 'yet', 'although', 'ley', 'everyone', 'last', 'someone', 'between', 'far', 'set', 'maybe', 'look', 'day', 'days', 'must', 'cly', 's', 'whose', 'quite', 'trying', 'saw', 'chapter', 'lak', 'dis', 'dey', 'wid', 'j', 'anyway', 'rather', 'towards', 'instead', 'along', 'twenty', 'half', 'turn', 'year', 'four', 'bring', 'took', 'hour', 'minute', 'except', 'end', 'lot', 'saying', 'ten', 'given', 'try', 'standing', 'word', 'until', 'somehow', 'week', 'keep', 'close', 'able', 'across', 'six', 'least', 'call', 'h', 'continued', 'two', 'already', 'n', 'people', 'sort', 'while', 'three', 'next', 'anything', 'without', 'beside', 'hundred', 'thousand', 'dor', 'sen', 'dak', 'amba', 'forward', 'watched', 'name', 'q', 'o', 'says', 'asked', 'dp'}


LOG_LOCATION = '/var/log/oireachtas_nlp/oireachtas_nlp.log' if os.getenv('TEST_ENV', 'False') == 'False' else '/tmp/test_oireachtas_nlp.log'

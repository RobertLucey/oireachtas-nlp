from itertools import chain
from collections import defaultdict

import tqdm

from oireachtas_data.utils import iter_debates
from oireachtas_data import members


def flatten(lst):
    """
    Given a nested list, flatten it.

    Usage:
        >>> flatten([[1, 2, 3], [1, 2]])
        [1, 2, 3, 1, 2]

    :param lst: list to be flattened
    :return: Flattened list
    """
    return list(chain.from_iterable(lst))


def get_speaker_para_map(only_groups=None):
    speaker_map = defaultdict(list)
    for debate in tqdm.tqdm(iter_debates()):
        for speaker, paras in debate.content_by_speaker.items():
            if only_groups is not None and speaker not in only_groups:
                continue
            speaker_map[speaker].extend(paras)

    return speaker_map


def get_party_para_map(only_groups=None):
    party_map = defaultdict(list)
    for debate in tqdm.tqdm(iter_debates()):
        for speaker, paras in debate.content_by_speaker.items():
            parties = members.parties_of_member(speaker)
            if parties is None or parties == []:
                continue
            for party in parties:
                if only_groups is not None and party not in only_groups:
                    continue
                party_map[party].extend(paras)

    return party_map

from itertools import chain


def flatten(lst):
    '''
    Given a nested list, flatten it.

    Usage:
        >>> flatten([[1, 2, 3], [1, 2]])
        [1, 2, 3, 1, 2]

    :param lst: list to be flattened
    :return: Flattened list
    '''
    return list(chain.from_iterable(lst))

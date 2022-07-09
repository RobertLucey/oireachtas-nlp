import argparse

from oireachtas_nlp.base_word_usage import (
    MemberWordUsage,
    PartyWordUsage
)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--group-by',
        dest='group_by',
        help='how to treat a group, by "member" or "party"',
        type=str,
        required=True
    )
    parser.add_argument(
        '--only-words',
        dest='only_words',
        help='a csv of words to exclusively look for',
        type=str
    )
    parser.add_argument(
        '--only-groups',
        dest='only_groups',
        help='a csv of groups to exclusively look for',
        type=str
    )
    parser.add_argument(
        '--top-n',
        dest='top_n',
        help='how many results to include',
        default=10,
        type=int
    )
    parser.add_argument(
        '--log-rate',
        dest='log_rate',
        help='how often to log results',
        default=100,
        type=int
    )

    args = parser.parse_args()

    only_words = None
    if args.only_words is not None:
        only_words = args.only_words.split(',')

    only_groups = None
    if args.only_groups is not None:
        only_groups = args.only_groups.split(',')

    if args.group_by == 'member':
        MemberWordUsage(
            only_words=only_words,
            only_groups=only_groups,
            head_tail_len=args.top_n,
            log_rate=args.log_rate
        ).process()
    elif args.group_by == 'party':
        PartyWordUsage(
            only_words=only_words,
            only_groups=only_groups,
            head_tail_len=args.top_n,
            log_rate=args.log_rate
        ).process()
    else:
        raise ValueError('group-type must be one of "member" or "party"')


if __name__ == '__main__':
    main()

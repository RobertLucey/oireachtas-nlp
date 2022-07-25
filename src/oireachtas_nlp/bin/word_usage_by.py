import argparse

from oireachtas_nlp.word_usage.member_word_usage import MemberWordUsage
from oireachtas_nlp.word_usage.party_word_usage import PartyWordUsage


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--min-paras-per-group",
        dest="min_paras_per_group",
        help="how mnay paragraphs must a group have to be processed",
        type=int,
        default=10,
    )
    parser.add_argument(
        "--group-by",
        dest="group_by",
        help='how to treat a group, by "member" or "party"',
        type=str,
        required=True,
    )
    parser.add_argument(
        "--only-words",
        dest="only_words",
        help="a csv of words to exclusively look for",
        type=str,
    )
    parser.add_argument(
        "--only-groups",
        dest="only_groups",
        help="a csv of groups to exclusively look for",
        type=str,
    )
    parser.add_argument(
        "--top-n",
        dest="top_n",
        help="how many results to include for each comparison",
        default=5,
        type=int,
    )
    parser.add_argument(
        "--include-government-words",
        dest="include_government_words",
        help="Include boring words like minister and deputy",
        action="store_true",
    )

    args = parser.parse_args()

    only_words = None
    if args.only_words is not None:
        only_words = args.only_words.split(",")

    only_groups = None
    if args.only_groups is not None:
        only_groups = args.only_groups.split(",")

    if args.group_by == "member":
        MemberWordUsage(
            only_words=only_words,
            only_groups=only_groups,
            head_tail_len=args.top_n,
            min_paras_per_group=args.min_paras_per_group,
            include_government_words=args.include_government_words,
        ).process()
    elif args.group_by == "party":
        PartyWordUsage(
            only_words=only_words,
            only_groups=only_groups,
            head_tail_len=args.top_n,
            min_paras_per_group=args.min_paras_per_group,
            include_government_words=args.include_government_words,
        ).process()
    else:
        raise ValueError('group-type must be one of "member" or "party"')


if __name__ == "__main__":
    main()

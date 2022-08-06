import argparse

import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

from oireachtas_nlp import logger
from oireachtas_nlp.utils import get_speaker_para_map, get_party_para_map


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--group-by",
        dest="group_by",
        type=str,
        required=True,
        choices=["member", "party"],
    )
    parser.add_argument(
        "--sort-by",
        dest="sort_by",
        type=str,
        required=True,
        choices=["neg", "pos", "neu"],
    )
    args = parser.parse_args()

    try:
        nltk.data.find("sentiment")
    except LookupError:  # pragma: nocover
        nltk.download("vader_lexicon")

    if args.group_by == "member":
        results = {}

        sia = SentimentIntensityAnalyzer()

        for speaker, paras in get_speaker_para_map(only_groups=None).items():
            # TODO: multiprocess?
            if len(paras) < 10:
                continue
            results[speaker] = sia.polarity_scores(
                "\n\n".join([p.content for p in paras])
            )

        sorted_key_results = sorted(
            results, key=lambda x: results[x][args.sort_by], reverse=True
        )

        for member in sorted_key_results:
            logger.info(f"{member.ljust(30)} {results[member]}")

    elif args.group_by == "party":
        results = {}

        sia = SentimentIntensityAnalyzer()

        for party, paras in get_party_para_map(only_items=None).items():
            # TODO: multiprocess?
            if len(paras) < 10:
                continue

            results[party] = sia.polarity_scores(
                "\n\n".join([p.content for p in paras])
            )

        sorted_key_results = sorted(
            results, key=lambda x: results[x][args.sort_by], reverse=True
        )

        for member in sorted_key_results:
            logger.info(f"{member.ljust(30)} {results[member]}")


if __name__ == "__main__":
    main()

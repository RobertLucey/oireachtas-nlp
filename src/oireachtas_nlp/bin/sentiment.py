import argparse
import multiprocessing
import random
from multiprocessing import Pool

import tqdm

import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

from oireachtas_nlp import logger
from oireachtas_nlp.utils import get_speaker_para_map, get_party_para_map


sia = SentimentIntensityAnalyzer()


def get_sentiment(item):
    if len(item[1]) < 5000:
        return (
            item[0],
            sia.polarity_scores(
                "\n\n".join([p.content for p in item[1]])
            )
        )
    else:
        return (
            item[0],
            sia.polarity_scores(
                "\n\n".join(random.sample([p.content for p in item[1]], 5000))
            )
        )


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
        data = get_speaker_para_map(only_groups=None)
    elif args.group_by == "party":
        data = get_party_para_map(only_groups=None)

    data = {k: v for k, v in data.items() if len(v) > 10}

    results = {}

    pool = Pool(processes=multiprocessing.cpu_count() - 1)
    for res in tqdm.tqdm(
        pool.imap_unordered(get_sentiment, data.items()),
        Gtotal=len(data)
    ):
        results[res[0]] = res[1]

    sorted_key_results = sorted(
        results, key=lambda x: results[x][args.sort_by], reverse=True
    )

    for k in sorted_key_results:
        logger.info(f"{k.ljust(30)} {results[k]}")


if __name__ == "__main__":
    main()

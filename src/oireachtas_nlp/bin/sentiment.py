import argparse
from collections import defaultdict

import tqdm
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

from oireachtas_data import members
from oireachtas_data.utils import iter_debates

from oireachtas_nlp import logger


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--group-by', dest='group_by', type=str, required=True, choices=['member', 'party'])
    parser.add_argument('--sort-by', dest='sort_by', type=str, required=True, choices=['neg', 'pos', 'neu'])
    args = parser.parse_args()

    try:
        nltk.data.find('sentiment')
    except LookupError:  # pragma: nocover
        nltk.download('vader_lexicon')

    if args.group_by == 'member':

        speaker_map = defaultdict(list)
        results = {}

        for debate in tqdm.tqdm(iter_debates()):
            for speaker, paras in debate.content_by_speaker.items():
                if members.get_member_from_name(speaker) is None:
                    continue
                speaker_map[speaker].extend(paras)

        sia = SentimentIntensityAnalyzer()

        for speaker, paras in tqdm.tqdm(speaker_map.items()):
            # TODO: multiprocess?
            if len(paras) < 10:
                continue
            results[speaker] = sia.polarity_scores('\n\n'.join([p.content for p in paras]))

        sorted_key_results = sorted(results, key=lambda x: results[x][args.sort_by], reverse=True)

        for member in sorted_key_results:
            logger.info(
                f'{member.ljust(30)} {results[member]}'
            )

    elif args.group_by == 'party':
        party_map = defaultdict(list)
        results = {}

        for debate in tqdm.tqdm(iter_debates()):
            for speaker, paras in debate.content_by_speaker.items():
                parties = members.parties_of_member(speaker)
                if parties is None or parties == []:
                    continue
                for party in parties:
                    party_map[party].extend(paras)

        sia = SentimentIntensityAnalyzer()

        for party, paras in tqdm.tqdm(party_map.items()):
            # TODO: multiprocess?
            if len(paras) < 10:
                continue

            results[party] = sia.polarity_scores('\n\n'.join([p.content for p in paras]))

        sorted_key_results = sorted(results, key=lambda x: results[x][args.sort_by], reverse=True)

        for member in sorted_key_results:
            logger.info(
                f'{member.ljust(30)} {results[member]}'
            )


if __name__ == '__main__':
    main()

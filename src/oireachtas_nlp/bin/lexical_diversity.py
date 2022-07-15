import argparse
from collections import defaultdict

import tqdm

from oireachtas_data import members
from oireachtas_data.utils import iter_debates

from oireachtas_nlp import logger
from oireachtas_nlp.models.para import ExtendedParas


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--group-by', dest='group_by', type=str, required=True, choices=['member', 'party'])
    args = parser.parse_args()

    if args.group_by == 'member':

        speaker_map = defaultdict(list)
        results = {}

        for debate in tqdm.tqdm(iter_debates()):
            for speaker, paras in debate.content_by_speaker.items():
                if members.get_member_from_name(speaker) is None:
                    continue
                speaker_map[speaker].extend(paras)

        for speaker, paras in tqdm.tqdm(speaker_map.items()):
            # TODO: multiprocess?
            if len(paras) < 10:
                continue

            extended_paras = ExtendedParas(data=paras)
            if len(extended_paras.text_obj.content) < 50000:
                continue

            diversity = extended_paras.text_obj.get_lexical_diversity(num_sample_words=50000)
            if diversity is not None:
                results[speaker] = diversity

        sorted_key_results = sorted(results, key=lambda x: results[x], reverse=True)

        logger.info('Logging results (the higher the number, the more diverse)')
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

        for party, paras in tqdm.tqdm(party_map.items()):
            # TODO: multiprocess?
            if len(paras) < 10:
                continue

            extended_paras = ExtendedParas(data=paras)
            if len(extended_paras.text_obj.content) < 50000:
                continue

            diversity = extended_paras.text_obj.get_lexical_diversity(num_sample_words=250000)
            if diversity is not None:
                results[party] = diversity

        sorted_key_results = sorted(results, key=lambda x: results[x], reverse=True)

        logger.info('Logging results (the higher the number, the more diverse)')
        for member in sorted_key_results:
            logger.info(
                f'{member.ljust(30)} {results[member]}'
            )


if __name__ == '__main__':
    main()

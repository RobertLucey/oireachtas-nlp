import argparse

from oireachtas_nlp import logger
from oireachtas_nlp.models.para import ExtendedParas
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
    args = parser.parse_args()

    if args.group_by == "member":
        results = {}
        for speaker, paras in get_speaker_para_map(only_groups=None).items():
            # TODO: multiprocess?
            if len(paras) < 10:
                continue

            extended_paras = ExtendedParas(data=paras)
            if len(extended_paras.text_obj.content) < 50000:
                continue

            diversity = extended_paras.text_obj.get_lexical_diversity(
                num_sample_words=50000
            )
            if diversity is not None:
                results[speaker] = diversity

        sorted_key_results = sorted(results, key=lambda x: results[x], reverse=True)

        logger.info("Logging results (the higher the number, the more diverse)")
        for member in sorted_key_results:
            logger.info(f"{member.ljust(30)} {results[member]}")

    elif args.group_by == "party":
        results = {}

        for party, paras in get_party_para_map(only_groups=None).items():
            # TODO: multiprocess?
            if len(paras) < 10:
                continue

            extended_paras = ExtendedParas(data=paras)
            if len(extended_paras.text_obj.content) < 50000:
                continue

            diversity = extended_paras.text_obj.get_lexical_diversity(
                num_sample_words=250000
            )
            if diversity is not None:
                results[party] = diversity

        sorted_key_results = sorted(results, key=lambda x: results[x], reverse=True)

        logger.info("Logging results (the higher the number, the more diverse)")
        for member in sorted_key_results:
            logger.info(f"{member.ljust(30)} {results[member]}")


if __name__ == "__main__":
    main()

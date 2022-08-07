import argparse

from oireachtas_data import members

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
    parser.add_argument(
        "--method",
        dest="method",
        type=str,
        required=True,
        choices=[
            "flesch_reading_ease",
            "flesch_kincaid_grade",
            "smog_index",
            "coleman_liau_index",
            "automated_readability_index",
            "dale_chall_readability_score",
            "difficult_words",
            "linsear_write_formula",
            "gunning_fog",
            "text_standard",
            "fernandez_huerta",
            "szigriszt_pazos",
            "gutierrez_polini",
            "crawford",
            "gulpease_index",
            "osman",
        ],
    )
    args = parser.parse_args()

    if args.group_by == "member":
        results = {}
        for speaker, paras in get_speaker_para_map(only_groups=None).items():
            # TODO: multiprocess?
            if len(paras) < 10:
                continue

            member = members.get_member_from_name(speaker)
            if member is None:
                continue

            extended_paras = ExtendedParas(data=paras)
            if len(extended_paras.text_obj.content) < 50000:
                continue

            difficulty = extended_paras.text_obj.get_reading_difficulty(args.method)
            if difficulty is not None:
                results[speaker] = difficulty

        sorted_key_results = sorted(results, key=lambda x: results[x], reverse=True)

        logger.info("Logging results")
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

            difficulty = extended_paras.text_obj.get_reading_difficulty(args.method)
            if difficulty is not None:
                results[party] = difficulty

        sorted_key_results = sorted(results, key=lambda x: results[x], reverse=True)

        logger.info("Logging results")
        for member in sorted_key_results:
            logger.info(f"{member.ljust(30)} {results[member]}")


if __name__ == "__main__":
    main()

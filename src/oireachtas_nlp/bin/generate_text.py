import os
import argparse
from random import shuffle

import gpt_2_simple as gpt2

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
        "--only-groups",
        dest="only_groups",
        help="a csv of groups (party name / member name) to exclusively look for",
        type=str,
    )
    parser.add_argument(
        "--sample",
        dest="sample",
        type=int,
        default=10000,
        help="How many sentences of each group to sample",
    )
    parser.add_argument("--num-epochs", dest="num_epochs", type=int, default=50)
    parser.add_argument("--shuffle", dest="shuffle", action="store_true")
    parser.add_argument(
        "--model", dest="model", default="124M", choices={"124M", "355M"}
    )

    args = parser.parse_args()

    # also group by general all text and bill types. Would be better for context

    only_groups = None
    if args.only_groups is not None:
        only_groups = args.only_groups.split(",")

    if args.group_by == "party" or args.group_by == "member":
        group_filter = (
            get_party_para_map if args.group_by == "party" else get_speaker_para_map
        )
        for subject, paras in group_filter(only_groups=only_groups).items():

            subject = subject.replace('á', 'a')

            print(f"Process: {subject}")

            extended_paras = ExtendedParas(data=paras)
            texts = extended_paras.text_obj.quick_sentences

            if len(texts) < 500:
                # Ignore without comment to reduce noise
                continue

            if len(texts) < args.sample:
                logger.warning(
                    f"{subject} has too few sentences to process. Consider lowering --sample"
                )
                continue

            if args.shuffle:
                shuffle(texts)

            texts = texts[: args.sample]

            file_text = "\n".join(texts)

            text_file_path = f"/tmp/{subject}.txt"
            with open(text_file_path, "w") as f:
                f.write(file_text)

            logger.info(f"Begin training: {subject}")

            model_dir = f"models_{subject}"
            if not os.path.isdir(model_dir):
                gpt2.download_gpt2(model_dir=model_dir, model_name=args.model)

            sess = gpt2.start_tf_sess()
            gpt2.finetune(
                sess,
                text_file_path,
                model_name=args.model,
                model_dir=model_dir,
                steps=args.num_epochs,
            )

            gpt2.generate(sess)

    else:
        raise Exception(f"Cannot group by {args.group_by}")


if __name__ == "__main__":
    main()

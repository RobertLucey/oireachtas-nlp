import argparse
import os
import sys
import multiprocessing

from gensim.models import Doc2Vec

from oireachtas_nlp import logger
from oireachtas_nlp.learn.tags import MemberTaggedDocs, PartyTaggedDocs
from oireachtas_nlp.learn.classifier import ClassifierCreator


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--compare-file", dest="compare_file", type=str, required=True)
    parser.add_argument(
        "--group-by",
        dest="group_by",
        type=str,
        required=True,
        choices=["member", "party"],
    )
    parser.add_argument("--epochs", dest="epochs", type=int, default=15)
    parser.add_argument("--min-per-group", dest="min_per_group", type=int, default=5000)
    parser.add_argument(
        "--max-per-group", dest="max_per_group", type=int, default=10000
    )
    parser.add_argument(
        "--doc2vec-minword", dest="doc2vec_minword", type=int, default=5
    )
    parser.add_argument("--window", dest="window", type=int, default=10)
    parser.add_argument("--vector-size", dest="vector_size", type=int, default=250)
    parser.add_argument("--negative", dest="negative", type=int, default=10)
    parser.add_argument(
        "--workers", dest="workers", type=int, default=multiprocessing.cpu_count() - 1
    )
    parser.add_argument("--train-ratio", dest="train_ratio", type=int, default=0.8)

    # TODO: specify a file of text content and see who why most sound like (other member / party)

    args = parser.parse_args()

    if not os.path.exists(args.compare_file):
        raise Exception("File at path does not exist: %s" % (args.compare_file))

    file_content = None
    with open(args.compare_file, "r") as fh:
        file_content = fh.read()

    if args.group_by == "member":
        tagged_docs = MemberTaggedDocs(
            min_per_group=args.min_per_group, max_per_group=args.max_per_group
        )
        tagged_docs.load_tagged_docs()
        tagged_docs.clean_data()
    elif args.group_by == "party":
        tagged_docs = PartyTaggedDocs(
            min_per_group=args.min_per_group, max_per_group=args.max_per_group
        )
        tagged_docs.load_tagged_docs()
        tagged_docs.clean_data()

    if len(tagged_docs.items) == 0:
        logger.warning("Reduce min_per_group to include some groups")
        sys.exit()

    model = Doc2Vec(
        min_count=args.doc2vec_minword,
        window=args.window,
        vector_size=args.vector_size,
        sample=1e-4,
        negative=args.negative,
        workers=args.workers,
    )

    classifier_creator = ClassifierCreator(
        model,
        tagged_docs,
        equalize_group_contents=True,
        train_ratio=args.train_ratio,
        epochs=args.epochs,
    )

    classifier_creator.generate_classifier()

    logger.info("Prediction:")
    logger.info(classifier_creator.predict(file_content))


if __name__ == "__main__":
    main()

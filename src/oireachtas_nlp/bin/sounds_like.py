import argparse
import os
import multiprocessing

from gensim.models import Doc2Vec

from oireachtas_data.utils import iter_debates

from oireachtas_nlp.learn.tags import MemberTaggedDocs
from oireachtas_nlp.learn.classifier import ClassifierCreator


class AltClassifierCreator(ClassifierCreator):

    def load_tagged_docs(self) -> None:
        processed = 0
        for debate in iter_debates():
            for speaker, paras in debate.content_by_speaker.items():

                if len(self.tagged_docs.items) >= self.num_items:
                    break

                # TODO:
                # The below should probably be in the tagged doc
                # map speakers to the pid "Bruce Wayne" -> "#BruceWayne"

                if speaker == '#':
                    continue
                if 'Comhairle' in speaker:
                    continue
                if 'Cathaoirleach' in speaker:
                    continue
                if 'Taoiseach' in speaker:
                    continue
                if '#' not in speaker:
                    continue

                content_str = '\n\n'.join(
                    [
                        p.content for p in paras
                    ]
                )

                if len(content_str) < 2000:
                    continue

                self.tagged_docs.load(speaker, paras)
                processed += 1


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--epochs',
        dest='epochs',
        default=15,
        type=int
    )
    parser.add_argument(
        '--num-items',
        dest='num_items',
        default=2**100,
        type=int
    )

    parser.add_argument(
        '--min-per-group',
        dest='min_per_group',
        default=250,
        type=int
    )

    parser.add_argument(
        '--doc2vec-minword',
        dest='doc2vec_minword',
        default=5,
        type=int
    )
    parser.add_argument(
        '--window',
        dest='window',
        default=10,
        type=int
    )
    parser.add_argument(
        '--vector-size',
        dest='vector_size',
        default=250,
        type=int
    )
    parser.add_argument(
        '--negative',
        dest='negative',
        default=10,
        type=int
    )
    parser.add_argument(
        '--workers',
        dest='workers',
        default=multiprocessing.cpu_count() - 1,
        type=int
    )

    parser.add_argument(
        '--compare-file',
        dest='compare_file',
        type=str,
        required=True
    )

    # TODO: specify a member and see who why most sound like (other member / party)
    # TODO: specify a file of text content and see who why most sound like (other member / party)

    args = parser.parse_args()

    if not os.path.exists(args.compare_file):
        raise Exception('File at path does not exist: %s' % (args.compare_file))

    file_content = None
    with open(args.compare_file, 'r') as fh:
        file_content = fh.read()

    classifier_creator = AltClassifierCreator(
        Doc2Vec(
            min_count=args.doc2vec_minword,
            window=args.window,
            vector_size=args.vector_size,
            sample=1e-4,
            negative=args.negative,
            workers=args.workers,
        ),
        MemberTaggedDocs(
            min_per_group=args.min_per_group
        ),
        num_items=args.num_items,
        equalize_group_contents=True,
        train_ratio=0.8,
        epochs=args.epochs
    )

    classifier_creator.generate_classifier()

    print('Prediction:')
    print(classifier_creator.predict(file_content))


if __name__ == '__main__':
    main()

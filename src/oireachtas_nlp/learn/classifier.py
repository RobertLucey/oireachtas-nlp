from collections import defaultdict

import numpy as np
from sklearn.neural_network import MLPClassifier

from oireachtas_nlp import logger
from oireachtas_nlp.learn.utils import get_train_test


def get_classifiers():
    return {"nnclassifier": MLPClassifier(alpha=1, max_iter=100000)}


class ClassifierCreator:
    def __init__(
        self,
        model,
        tagged_docs,
        equalize_group_contents=False,
        train_ratio=0.8,
        epochs=10,
    ):
        """

        :param model: An init'd Doc2Vec model
        :param tagged_docs: class of tagged docs.
            Books given to this will be split by some tag.
            Example: NationalityTaggedDocs will split books into the
                     nationality of the author
        :kwarg equalize_group_contents: Ensure that the number of items in each
            tag are proportional. Will chop the excess from groups with more
            items than the minimum
        :kwarg train_ratio: What proportion to use for training
        :kwarg epochs: How many epochs to train whatever the given model is
        """
        self.model = model
        self.tagged_docs = tagged_docs
        self.equalize_group_contents = equalize_group_contents
        self.train_ratio = train_ratio
        self.epochs = epochs

        self.classifiers = {}
        self.class_group_map = {}

    def generate_classifier(self):

        logger.info("Using %s tagged docs" % (len(self.tagged_docs.items)))

        logger.info("Start loading content into model")
        self.model.build_vocab(self.tagged_docs.to_array())
        logger.info("Finished loading content into model")

        logger.info("Start training model")

        self.model.train(
            self.tagged_docs.perm(),
            total_examples=self.model.corpus_count,
            epochs=self.epochs,
        )
        print("Finished training model")

        grouped_vecs = defaultdict(list)
        for tag in self.model.docvecs.key_to_index.keys():
            if len(tag.split("_")) > 2:
                continue
            grouped_vecs[tag.split("_")[0]].append(int(tag.split("_")[1]))

        print("Creating train/test set")
        (
            train_arrays,
            train_labels,
            test_arrays,
            test_labels,
            class_group_map,
        ) = get_train_test(
            self.model,
            grouped_vecs,
            equalize_group_contents=self.equalize_group_contents,
            train_ratio=self.train_ratio,
        )
        print("Created train/test set")

        classifiers = get_classifiers()

        for name, clf in classifiers.items():
            try:
                print("----------")
                clf.fit(train_arrays, train_labels)
                score = clf.score(test_arrays, test_labels)
                print("%s %s" % (name, score))

                joined = [i for i in zip(test_labels, test_arrays)]
                class_arrays_map = defaultdict(list)
                for test_label, test_array in joined:
                    class_arrays_map[test_label].append(test_array)

                for label, array in class_arrays_map.items():
                    score = clf.score(np.array(array), len(array) * [label])
                    print("%s %s" % (class_group_map[label], score))

                print("----------")

                classifiers[name] = clf
            except ValueError as ex:
                print('Failed to use classifier "%s": %s' % (name, ex))
                classifiers[name] = None

        self.classifiers = classifiers
        self.class_group_map = class_group_map

        # TODO: get the best classifier and use that in future
        self.preferred_classifier = self.classifiers["nnclassifier"]

    def predict(self, content: str):
        return self.class_group_map[
            self.preferred_classifier.predict(
                [self.model.infer_vector(content.split())]
            )[0]
        ]

from unittest import TestCase, skip

from gensim.models import Doc2Vec
from gensim.models.doc2vec import TaggedDocument

from oireachtas_nlp.learn.utils import get_train_test


class LearnUtilsTest(TestCase):
    def test_get_train_test(self):

        tagged_docs = [
            TaggedDocument(["word", "word"], ["a_0"]),
            TaggedDocument(["word", "word"], ["a_1"]),
            TaggedDocument(["word", "word"], ["a_2"]),
            TaggedDocument(["word", "word"], ["b_0"]),
            TaggedDocument(["word", "word"], ["b_1"]),
            TaggedDocument(["word", "word"], ["b_2"]),
            TaggedDocument(["word", "word"], ["c_0"]),
            TaggedDocument(["word", "word"], ["c_1"]),
            TaggedDocument(["word", "word"], ["c_2"]),
        ]

        model = Doc2Vec(
            min_count=5, window=10, vector_size=150, sample=1e-4, negative=5, workers=2
        )

        model.build_vocab(tagged_docs)

        grouped_vecs = {
            "a": [0, 1, 2],
            "b": [0, 1, 2],
            "c": [0, 1, 2],
        }

        (
            train_arrays,
            train_labels,
            test_arrays,
            test_labels,
            class_group_map,
        ) = get_train_test(
            model, grouped_vecs, equalize_group_contents=False, train_ratio=0.8
        )

        self.assertEqual(len(train_arrays), 6)
        self.assertEqual(train_labels.tolist(), [0, 0, 1, 1, 2, 2])
        self.assertEqual(test_labels.tolist(), [0, 1, 2])

        self.assertEqual(class_group_map, {0: "a", 1: "b", 2: "c"})

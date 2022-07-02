from unittest import TestCase
from mock import patch

from oireachtas_nlp.models.text import TextBody
from oireachtas_nlp.learn.base_tagged_docs import BaseTaggedDocs


class BaseTaggedDocsTest(TestCase):

    @patch(
        'oireachtas_nlp.learn.base_tagged_docs.BaseTaggedDocs.should_include',
        side_effect=lambda x: True
    )
    def test_load(self, mock_should_include):
        docs = BaseTaggedDocs()
        docs.load('speaker_name', 'content')
        self.assertEqual(
            docs.items,
            [('speaker_name', 'content')]
        )

    @patch(
        'oireachtas_nlp.learn.base_tagged_docs.BaseTaggedDocs.should_include',
        side_effect=lambda x: True
    )
    @patch(
        'oireachtas_nlp.learn.base_tagged_docs.BaseTaggedDocs.get_group_name',
        side_effect=lambda x: True
    )
    def test_iter(self, mock_group_name, mock_should_include):
        docs = BaseTaggedDocs()
        docs.load('speaker_1', [TextBody(content='content_1')])
        docs.load('speaker_2', [TextBody(content='content_2')])
        res = [i for i in docs]
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0].tags, ['speaker_1_0'])
        self.assertEqual(res[0].words, ['content_1'])

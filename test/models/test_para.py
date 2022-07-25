from unittest import TestCase

from oireachtas_data.models.para import Para

from oireachtas_nlp.models.para import ExtendedParas
from oireachtas_nlp.models.text import TextBody


class ParaTest(TestCase):
    def test_text_obj(self):
        para = ExtendedParas(
            data=[
                Para(
                    title="title 1", eid=None, content="This is the content of title 1"
                ),
                Para(
                    title="title 2", eid=None, content="This is the content of title 2"
                ),
            ]
        )

        self.assertIsInstance(para.text_obj, TextBody)

from oireachtas_data.models.para import Paras

from oireachtas_nlp.models.text import TextBody


class ExtendedParas(Paras):
    @property
    def text_obj(self):
        return TextBody(content=" \n".join([p.content for p in self.data]))

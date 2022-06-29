from gensim.models.doc2vec import TaggedDocument

from oireachtas_nlp.models.text import TextBody
from oireachtas_nlp.learn.base_tagged_docs import BaseTaggedDocs


class MemberTaggedDocs(BaseTaggedDocs):

    def __iter__(self):
        for speaker, paras in self.items:

            if '%' in speaker:
                continue

            if speaker.strip() == '#':
                continue

            body = TextBody(content='\n\n'.join(
                [p.content for p in paras]
            ))
            yield TaggedDocument(
                self.content_cleaner(body).split(),
                [str(speaker + '_%s') % (self.counter[speaker])]
            )
            self.counter[speaker] += 1

    def get_group_name(self, item) -> int:
        return item[0]

    def should_include(self, debate):
        return True

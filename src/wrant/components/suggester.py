import spacy
from ..utils import util

'''
from wrant.components.preprocessor import Preprocessor
from wrant.components.suggester import Suggester
suggester = Suggester(Preprocessor.load())
'''
class Suggester:
    START = '<START>'
    END = '<END>'

    def __init__(self, corpus, nlp=None):
        if not nlp:
            nlp = spacy.load('en')
        self.nlp = nlp
        self.corpus = corpus
        self._create_context()

    def _context(self, i, sent):
        prev = sent[i-1].lower_ if i > 0 else self.START
        token = sent[i].lower_
        next = sent[i+1].lower_ if i < len(sent)-1 else self.END
        return prev, token, next

    @staticmethod
    def _add(dict, key, val):
        if key not in dict:
            dict[key] = set()
        dict[key].add(val)

    def _create_context(self):
        context = {}
        rev_context = {}
        for sent in self.corpus.sents:
            for i in range(len(sent)):
                prev, token, next = self._context(i, sent)
                self._add(context, token, (prev, next))
                self._add(rev_context, (prev, next), token)
        self.context = context
        self.rev_context = rev_context

    def check_doc(self, text):
        pass

    def suggest(self, text):
        doc = self.nlp(text)
        sentence = ''
        suggestions = {}
        for sent in doc.sents:
            for i in range(len(sent)):
                suggest = False
                t = sent[i]
                prev, token, next = self._context(i, sent)
                if token not in self.context:
                    sentence += util.red(t.string)
                    suggest = True
                elif (prev, next) not in self.context[token]:
                    sentence += util.yellow(t.string)
                    suggest = True
                else:
                    sentence += util.green(t.string)

                if suggest and (prev, next) in self.rev_context:
                        suggestions[token] = self.rev_context[(prev, next)]
        print(sentence)
        print(suggestions)

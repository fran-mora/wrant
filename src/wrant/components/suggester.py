import spacy
from pprint import pprint
from ..utils import util
import time

'''
from wrant.components.suggester import Suggester
suggester = Suggester()
'''
class Suggester:
    START = '<START>'
    END = '<END>'

    def __init__(self, load=True, nlp=None):
        start = time.time()
        if not nlp:
            nlp = spacy.load('en')
        self.nlp = nlp
        if load:
            contexts = util.load('./data/contexts.pkl')
            self.context = contexts[0]
            self.rev_context = contexts[1]
        print('loaded in ' + util.lapsed(start))

    @staticmethod
    def _clean(token):
        return token.text.lower() if token.tag_ != 'NNP' else 'NNP'

    def _context(self, i, sent):
        prev = self._clean(sent[i-1]) if i > 0 else self.START
        token = self._clean(sent[i])
        next = self._clean(sent[i+1]) if i < len(sent)-1 else self.END
        return prev, token, next

    @staticmethod
    def _add(dict, key, val):
        if key not in dict:
            dict[key] = {}
        if val not in dict[key]:
            dict[key][val] = 0
        dict[key][val] += 1

    def _create_context(self, sents):
        context = {}
        rev_context = {}

        for sent in sents:
            for i in range(len(sent)):
                prev, token, next = self._context(i, sent)
                self._add(context, token, (prev, next))
                self._add(rev_context, (prev, next), token)
        self.context = context
        self.rev_context = rev_context

    def _store(self):
        contexts = (self.context, self.rev_context)
        util.save(contexts, './data/contexts.pkl')

    def check_doc(self, text):
        pass

    def _top(self, key, topn):
        dict = self.rev_context[key]
        ordered = util.sortdict(dict, rev=True)
        return ordered[:topn] if len(ordered) >= topn else ordered

    def suggest(self, text):
        doc = self.nlp(text)
        sentence = ''
        suggestions = []
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
                        suggestions.append((token, self._top((prev, next), 3)))
        print(sentence)
        pprint(suggestions)

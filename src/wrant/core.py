from .nlp import Token
from .components.concordance import Concorder
from .components.suggesting import Suggester
from .utils import util

class Wrant:

    def __init__(self, nlp, sents):
        self.nlp = nlp
        self.tokens = []  # single list of tokens of the whole corpus
        for sent in sents:
            for tok in sent:
                self.tokens.append(tok)

        print('Building components:')
        start = util.time.time()
        # print('\t- concordance')
        # self.concorder = Concorder(self.tokens)
        print('\t- suggesting')
        self.suggester = Suggester(self.tokens)
        print(f'Done in {util.lapsed(start)}')

    def concordance(self, frag):
        self.concorder.concord(self.nlp(frag))

    def check(self, frag):
        self.suggester.check(self.nlp(frag))

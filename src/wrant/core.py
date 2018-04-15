from .components.concordance import Concorder
from .components.suggesting import Suggester
from .components.verbs_prep import VerbPrep
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
        print('\t- concordance')
        self.concorder = Concorder(self.tokens)
        print('\t- suggesting')
        self.suggester = Suggester(self.tokens)
        print('\t- verbs_prep')
        self.verbs_prep = VerbPrep()
        print(f'Done in {util.lapsed(start)}')

    def concordance(self, frag):
        self.concorder.concord(self.nlp(frag))

    def check(self, frag):
        # self.suggester.check(self.nlp(frag))
        return self.verbs_prep.check(self.nlp(frag))

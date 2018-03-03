from .nlp import Token
from .components.concordance import Concorder
from .utils import util

class Wrant:

    def __init__(self, nlp, sents):
        self.nlp = nlp
        print('Building components:')
        start = util.time.time()
        print('\t- concordance')
        self.concorder = Concorder(sents)
        print(f'Done in {util.lapsed(start)}')

    def concordance(self, frag):
        self.concorder.concord(self.nlp(frag))

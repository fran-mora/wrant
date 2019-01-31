from old.nltk_ext import ConcordanceIndex
from tqdm import tqdm

from .components.concordance import Concorder
from .components.suggesting import Suggester
from .components.verbs_prep import VerbPrep
from .utils import util


class Wrant:

    def __init__(self, nlp, sents):
        self.nlp = nlp
        self.tokens = []  # single list of tokens of the whole corpus
        self.lemmas = []
        for sent in tqdm(sents):
            for tok in sent:
                if '\n' not in tok.text:
                    self.tokens.append(tok.text)
                    self.lemmas.append(tok.lemma_)

        self._concorder = ConcordanceIndex(self.tokens, self.lemmas, self.nlp)
        # print('\t- suggesting')
        # self.suggester = Suggester(self.tokens)
        #print('\t- verbs_prep')
        #self.verbs_prep = VerbPrep()

    def concordance(self, words, context=None, context_size=5, width=75, lines=25):
        self._concorder.print_concordance(words, context=context, context_size=context_size, width=width, lines=lines)

    def check(self, frag):
        # self.suggester.check(self.nlp(frag))
        return self.verbs_prep.check(self.nlp(frag))

import spacy
from .concordance import ConcordanceIndex
from .util import load
from .constants import CORPUS


class Wrant:

    def __init__(self):
        print('Loading resources...')
        corpus = load(CORPUS)
        nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
        self.concorder = ConcordanceIndex(corpus['tokens'], corpus['lemmas'], nlp)

    def concordance(self, text, width=75, lines=25, lemma=True, context=None, context_size=5):
        self.concorder.print_concordance(
            text,
            width=width,
            lines=lines,
            lemma=lemma,
            context=context,
            context_size=context_size
        )


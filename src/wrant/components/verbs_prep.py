from wrant.utils import util, str_util
from wrant.constants import DATA_DIR


class VerbPrep:

    def __init__(self):
        self.verbs = util.load(f'{DATA_DIR}/verbs_prep.pkl')

    def _check_prep(self, tok, prep, verb_lemma, highlights):
        if prep.lemma_ not in self.verbs[verb_lemma]:
            highlights.append((tok.idx, tok.idx + len(tok), 'red'))
            highlights.append((prep.idx, prep.idx + len(prep), 'red'))
        else:
            highlights.append((tok.idx, tok.idx + len(tok), 'green'))
            highlights.append((prep.idx, prep.idx + len(prep), 'green'))

    def _check(self, tok, highlights):
        if tok.pos_ == 'VERB':
            verb_lemma = tok.lemma_
            prt = str_util.get_by_dep(tok.children, 'prt')
            prep = str_util.get_by_dep(tok.children, 'prep')
            if prt:
                verb_lemma += '_' + prt.lemma_

            if verb_lemma not in self.verbs:
                highlights.append((tok.idx, tok.idx + len(tok), 'grey'))
                return

            if prep:
                self._check_prep(tok, prep, verb_lemma, highlights)

    def check(self, doc):
        highlights = []
        for tok in doc:
            self._check(tok, highlights)
        return highlights

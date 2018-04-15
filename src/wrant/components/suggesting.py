from collections import defaultdict
from ..utils import util

LOOK_AHEAD = 5


class Suggester:

    def __init__(self, tokens):
        self.tokens = tokens
        self._build_index()

    def _word_repr(self, tok):
        if tok.tag_ in ['NNP', 'CD']:
            return tok.tag_
        return tok.text.lower()

    def _build_index(self):
        self.offsets = defaultdict(list)  # dictionary of token offsets in text

        for i, tok in enumerate(self.tokens):
            word = self._word_repr(tok)
            self.offsets[word].append(i)

    def _score(self, tok):
        max_score = 0
        doc = tok.doc
        for offset in self.offsets[self._word_repr(tok)]:
            score = 0
            # look back
            for i, t in enumerate(reversed(doc[:tok.i])):
                index = i-1
                if (
                    offset - index < 0 or
                    self._word_repr(t) !=
                    self._word_repr(self.tokens[offset-index])
                ):
                    break
                score += 1
            # look forward
            for i, t in enumerate(doc[tok.i:]):
                if (
                    offset+i >= len(self.tokens) or
                    self._word_repr(t) !=
                    self._word_repr(self.tokens[offset+i])
                ):
                    break
                score += 1
            max_score = max(max_score, score)
        return max_score

    def check(self, frag_doc):
        start = util.time.time()
        checked = []
        for tok in frag_doc:
            score = self._score(tok)
            checked.append(
                f'{tok.text}[{util.blue(str(score))}]{tok.whitespace_}'
            )
        print(''.join(checked))
        print(util.lapsed(start))

from collections import defaultdict
from ..utils import util


class Concorder:

    def __init__(self, sents):
        self._build_index(sents)

    def _build_index(self, sents):
        self.text = []  # single list of tokens of the whole corpus
        self.offsets = defaultdict(list)  # dictionary of token offsets in text

        for sent in sents:
            for tok in sent:
                self.text.append(tok)
                self.offsets[tok.lemma_].append(len(self.text) - 1)

    def _match(self, offset, tokens):
        if offset + len(tokens) > len(self.text):
            return False

        for i,tok in enumerate(tokens):
            if tok.text == '?':
                return (
                    self._match(offset+i, tokens[i+1:]) or
                    self._match(offset+i+1, tokens[i+1:]
                )
            elif tok.lemma_ != self.text[offset+i].lemma_:
                return False
        return True


    def _get_offsets(self, frag_doc):
        word = frag_doc[0].lemma_
        return [
            offset for offset in self.offsets[word]
            if self._match(offset, frag_doc)
        ]


    def concord(self, frag_doc, width=100, lines=25):
        half_width = (width - len(frag_doc.text) - 2) // 2
        cont = width // 4 # approx number of words of context
        size = len(frag_doc)

        offsets = self._get_offsets(frag_doc)
        if offsets:
            lines = min(lines, len(offsets))
            print(f'Displayed {lines} of {len(offsets)} matches.')
            for i in offsets[:lines]:
                left = (' ' * half_width +
                        ' '.join([tok.text for tok in self.text[i-cont:i]]))
                right = ' '.join([tok.text for tok in self.text[i+size:i+cont]])
                left = left[-half_width:]
                right = right[:half_width]
                mid = ' '.join([tok.text for tok in self.text[i:i+size]])
                result = f'{left} {util.bold(mid)} {right}'.replace('\n', '')
                print(result)
        else:
            print("No matches")

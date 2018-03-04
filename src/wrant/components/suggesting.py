from collections import defaultdict
from ..utils import util
from tqdm import tqdm

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
        # unigrams = set()
        # for i in tqdm(range(len(self.tokens))):
        #     unigrams.add(self._word_repr(self.tokens[i]))
        # words_int = dict()
        # unigrams_list = list(unigrams)
        # unigrams = None
        # for i in range(len(unigrams_list)):
        #     words_int[unigrams_list[i]] = i
        # int_words = {}
        # for word,i in words_int.items():
        #     int_words[i] = word
        # bigrams = set()
        # for i in tqdm(range(len(self.tokens)-2)):
        #     bigrams.add(tuple([words_int[self._word_repr(tok)] for tok in self.tokens[i:i+2]]))
        # trigrams = set()
        # for i in tqdm(range(len(self.tokens)-3)):
        #     trigrams.add(tuple([words_int[self._word_repr(tok)] for tok in self.tokens[i:i+3]]))
        # quadrigrams = set()
        # for i in tqdm(range(len(self.tokens)-4)):
        #     quadrigrams.add(tuple([words_int[self._word_repr(tok)] for tok in self.tokens[i:i+4]]))
        # quintigrams = set()
        # for i in tqdm(range(len(self.tokens)-5)):
        #     quintigrams.add(tuple([words_int[self._word_repr(tok)] for tok in self.tokens[i:i+5]]))
        #
        # ngrams = {
        #     'int_words': int_words,
        #     'bigrams': bigrams,
        #     'trigrams': trigrams,
        #     'quadrigrams': quadrigrams,
        #     'quintigrams': quintigrams
        # }
        # util.save(ngrams, 'data/ngrams.pkl')
        # self.trigrams = trigrams

    def _score(self, tok):
        max_score = 0
        doc = tok.doc
        for offset in self.offsets[self._word_repr(tok)]:
            score = 0
            # look back
            for i,t in enumerate(reversed(doc[:tok.i])):
                index = i-1
                if (
                    offset - index < 0 or
                    self._word_repr(t) != self._word_repr(self.tokens[offset-index])
                ):
                    break
                score += 1
            # look forward
            for i,t in enumerate(doc[tok.i:]):
                if (
                    offset+i >= len(self.tokens) or
                    self._word_repr(t) != self._word_repr(self.tokens[offset+i])
                ):
                    break
                score += 1
            max_score = max(max_score, score)
        return max_score

    # def _score_trigrams(self, tok):
    #     if tok.i <= 0 or tok.i == len(tok.doc) - 1:
    #         return 0
    #     doc = tok.doc
    #     i = tok.i
    #     trigram = (self._word_repr(doc[i-1]), self._word_repr(tok), self._word_repr(doc[i+1]))
    #     return trigram in self.trigrams

    def check(self, frag_doc):
        start = util.time.time()
        checked = []
        for tok in frag_doc:
            score = self._score(tok)
            checked.append(f'{tok.text}[{util.blue(str(score))}]{tok.whitespace_}')
        print(''.join(checked))
        print(util.lapsed(start))

from collections import defaultdict
from tqdm import tqdm
from wrant.constants import DATA_DIR
from wrant.utils import util


def gen_ngrams():
    print('Loading sentences')
    sents = util.load(f'{DATA_DIR}/sents.pkl')
    unigrams = defaultdict(int)
    bigrams = defaultdict(int)
    trigrams = defaultdict(int)
    print('Computing ngrams')
    for sent in tqdm(sents):
        for i, tok in enumerate(sent):
            prev = sent[i-1].text.lower() if i > 0 else '<start>'
            curr = tok.text.lower()
            next = sent[i+1].text.lower() if i < len(sent)-1 else '<end>'
            unigrams[curr] += 1
            bigrams[(prev, curr)] += 1
            trigrams[(prev, curr, next)] += 1
        bigrams[(curr, next)] += 1

    print('Saving')
    util.save(unigrams, f'{DATA_DIR}/produced/unigrams.pkl')
    util.save(bigrams, f'{DATA_DIR}/produced/bigrams.pkl')
    util.save(trigrams, f'{DATA_DIR}/produced/trigrams.pkl')

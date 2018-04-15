import spacy
from .core import Wrant
from .utils import util
from .constants import DATA_DIR


def create_wrant():
    nlp = spacy.load('en', disable=['ner', 'parse'])
    print('Loading corpus')
    start = util.time.time()
    corpus = util.load(f'{DATA_DIR}/corpus.pkl')
    print(f'Done in {util.lapsed(start)}')
    print('Building corpus')
    start = util.time.time()
    sents = []
    int_tokens = corpus['int_tokens']
    for sent in corpus['sents']:
        sent = [int_tokens[i] for i in sent]
        sents.append(sent)
    print(f'Done in {util.lapsed(start)}')
    return Wrant(nlp, sents)

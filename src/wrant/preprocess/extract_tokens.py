import spacy
from tqdm import tqdm
from ..utils import util, str_util
from ..nlp import Token
from ..constants import DATA_DIR


def _token_id(token, tokens_int):
    tok = Token(token.text, token.tag_, token.lemma_)
    if tok not in tokens_int:
        tokens_int[tok] = len(tokens_int)
    return tokens_int[tok]


def _sentences(doc, tokens_int):
    sents = []
    for s in doc.sents:
        sent = [_token_id(token, tokens_int) for token in s]
        sents.append(sent)
    return sents


def process():
    nlp = spacy.load('en', disable=['ner'])
    texts = str_util.get_corpus()

    print('Spacyfing corpus')
    sents = []
    tokens_int = {}

    for text in tqdm(texts):
        sents += _sentences(nlp(text), tokens_int)
    print('Done')

    int_tokens = {}
    for k, v in tokens_int.items():
        int_tokens[v] = k
    corpus = {
        'sents': sents,
        'tokens_int': tokens_int,
        'int_tokens': int_tokens,
    }
    print('Storing results')
    util.save(corpus, f'{DATA_DIR}/corpus.pkl')

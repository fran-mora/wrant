import re
import spacy
from spacy.tokens import Doc
from spacy.vocab import Vocab
from tqdm import tqdm
import os
import time
from ..utils import util
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

def _normalise(text):
    text = text.replace('”','"').replace('“','"').replace('’',"'").replace('`',"'")
    text = text.replace('—','-').replace('…','...').replace('‘',"'")
    text = re.sub('\n+','\n', text)
    return text

def process():
    nlp = spacy.load('en', disable=['ner'])
    print('Reading corpus')
    dir = f'{DATA_DIR}/books/'
    texts = []
    for filename in tqdm(util.files(dir)[:]):
        texts.append(_normalise(util.read(dir + filename)))

    print('Spacyfing corpus')
    sents = []
    tokens_int = {}

    for text in tqdm(texts):
        sents += _sentences(nlp(text), tokens_int)
    print('Done')

    int_tokens = {}
    for k,v in tokens_int.items():
        int_tokens[v] = k
    corpus = {
        'sents': sents,
        'tokens_int': tokens_int,
        'int_tokens': int_tokens,
    }
    print('Storing results')
    util.save(corpus, f'{DATA_DIR}/corpus.pkl')

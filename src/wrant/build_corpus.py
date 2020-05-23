#!/usr/bin/env python3
from .util import files, read, save
import spacy
from tqdm import tqdm
from .constants import BOOKS_DIR, CORPUS


def normalise(text):
    text = text.replace('”', '"')\
        .replace('“', '"')\
        .replace('’', "'")\
        .replace('—', '-')\
        .replace('…', '...')\
        .replace('`', "'")\
        .replace('‘', "'")
    return text


def build():
    print('Reading...')
    text = ''
    cnt = 0
    for filename in files(BOOKS_DIR):
        if not filename[0].startswith('.'):
            cnt += 1
            text += read(BOOKS_DIR + filename) + '\n'

    print(f'{cnt} books read.')
    print('Normalising punctuation...')
    text = normalise(text)
    print('Done.')

    nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
    tokens = []
    lemmas = []
    print('Tokenizing and lemmatizing...')
    for line in tqdm(text.split('\n')[:1000]):
        line = line.strip()
        if line:
            doc = nlp(line)
            for tok in doc:
                tokens.append(tok.text)
                lemmas.append(tok.lemma_)

    print('Saving...')
    save({
        'tokens': tokens,
        'lemmas': lemmas
    }, CORPUS)
    print('Done.')


if __name__ == '__main__':
    build()

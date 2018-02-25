#!/usr/bin/env python3
import os
from util import *
import nltk
import sys
import time
from nltk.stem import WordNetLemmatizer


def reduce_pos(pos):
    return 'v' if pos[0:2] == 'VB' else 'n'

def normalise(text):
    text = text.replace('”','"').replace('“','"').replace('’',"'").replace('—','-').replace('…','...').replace('`',"'").replace('‘',"'")
    return text

print('Reading...')
text = ''
cnt = 0
for filename in os.listdir('books/'):
    if not filename[0] == '.':
        cnt += 1
        text += read('books/' + filename) + '\n'


print(f'{cnt} books read.')
lemmatizer = WordNetLemmatizer()
print('Normalising punctuation...')
text = normalise(text)

print('Sentence splitting... ',end='')
start = time.time()
text_tmp = text.replace('\n',' ')
sentences = nltk.sent_tokenize(text_tmp)
print('done [' + lapsed(start) + ']')
print('Size of sents: ' + str(len(sentences)))

print('Tokenizing and Pos tagging...')
start = time.time()
sents = []
for i in range(len(sentences)):
    if i % 10000 == 0:
        print(percent(i, len(sentences)) + ' done [' + lapsed(start) + ']')

    sent = sentences[i]
    sents.append(nltk.pos_tag(nltk.word_tokenize(sent)))

print('Post processing...')
toks = ''
poss = ''
for sent in sents:
    for tok in sent:
        lemma = lemmatizer.lemmatize(tok[0], pos=reduce_pos(tok[1]))
        toks += tok[0] + ' '
        poss += tok[0] + '/' + tok[1] + '/' + lemma + ' '
    toks += '\n'
    poss += '\n'

print('Writing...')
write(text, 'corpus.txt')
write(toks, 'corpus_tok.txt')
write(poss, 'corpus_pos_lem.txt')
print('Done...')

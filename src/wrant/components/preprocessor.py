import re
import spacy
from spacy.tokens import Doc
from spacy.vocab import Vocab
from tqdm import tqdm
import os
import time
from ..utils import util
from ..nlp.token import Token
'''
from wrant.components.preprocessor import Preprocessor
prep = Preprocessor()
prep.preprocess()
'''
class Preprocessor:

    def __init__(self, dir='./data/'):
        self.nlp = spacy.load('en', parse=True)
        self.dir = dir

    def preprocess(self):
        self._create_corpus()
        self._w2v()
        self._store()

    @staticmethod
    def _sentences(doc):
        sents = []
        for s in doc.sents:
            sent = [Token(token) for token in s]
            sents.append(sent)
        return sents

    def _create_corpus(self):
        print('Creating corpus')
        self.sents = []
        dir = self.dir + 'books/'
        for filename in tqdm(util.files(dir)):
            text = self.normalise(util.read(dir + filename))
            doc = self.nlp(text)
            self.sents += self._sentences(doc)

    # def _nlp(self):
    #     print('Spacyfing corpus, this will take a long while...')
    #     start = time.time()
    #     self.doc = self.nlp(self.corpus)
    #     print(f'Done in {util.lapsed(start)}')

    def _w2v(self):
        print('Creating word2vec model')
        start = time.time()
        # TODO

    def _store(self):
        print('Storing results')
        util.save(self.sents, self.dir + 'sents.pkl')
        # TODO: w2v

    def load(self):
        start = time.time()
        self.sents = util.load(self.dir + 'sents.pkl')
        print(util.lapsed(start))
        return self.sents

    @staticmethod
    def normalise(text):
        text = text.replace('”','"').replace('“','"').replace('’',"'").replace('—','-').replace('…','...').replace('`',"'").replace('‘',"'")
        text = re.sub('\n+','\n', text)
        return text

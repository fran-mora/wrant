import spacy
from spacy.tokens import Doc
from spacy.vocab import Vocab
from tqdm import tqdm
import os
import time
from ..utils import util

'''
from wrant.components.preprocessor import Preprocessor
prep = Preprocessor()
prep.preprocess()
'''
class Preprocessor:

    def __init__(self, dir='./data/books/'):
        self.nlp = spacy.load('en')
        self.dir = dir

    def preprocess(self):
        self._create_corpus()
        self._nlp()
        self._w2v()
        self._store()

    def _create_corpus(self):
        print('Creating corpus')
        self.corpus = ''
        for filename in tqdm(os.listdir(self.dir)):
            if not filename[0] == '.':
                self.corpus += util.read(self.dir + filename) + '\n'

        # normalise
        print('Normalising corpus')
        self.corpus = self.normalise(self.corpus)

    def _nlp(self):
        print('Spacyfing corpus, this will take a long while...')
        start = time.time()
        self.doc = self.nlp(self.corpus)
        print(f'Done in {util.lapsed(start)}')

    def _w2v(self):
        print('Creating word2vec model')
        start = time.time()
        # TODO

    def _store(self):
        print('Storing results')
        self.doc.to_disk('./data/doc.bin')
        self.doc.vocab.to_disk('./data/vocab.bin')
        # TODO: w2v

    @staticmethod
    def load():
        vocab = Vocab().from_disk('./data/vocab.bin')
        corpus = Doc(vocab).from_disk('./data/doc.bin')
        # TODO: w2v
        return corpus

    @staticmethod
    def normalise(text):
        text = text.replace('”','"').replace('“','"').replace('’',"'").replace('—','-').replace('…','...').replace('`',"'").replace('‘',"'")
        return text

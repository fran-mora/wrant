import spacy
from ..utils import util

class Preprocesser:

    def __init__(self, dir='./data/books/'):
        self.nlp = spacy.load('en')
        self.dir = dir

    def preprocess():
        self._create_corpus()
        self._nlp()
        self._w2v()

    def _create_corpus():
        self.corpus = ''
        for filename in os.listdir(self.dir):
            if not filename[0] == '.':
                cnt += 1
                self.corpus += util.read(self.dir + filename) + '\n'

        # normalise
        self.corpus = self.normalise(self.corpus)

    def _nlp():
        pass

    def _w2v():
        pass


    def normalise(text):
        text = text.replace('”','"').replace('“','"').replace('’',"'").replace('—','-').replace('…','...').replace('`',"'").replace('‘',"'")
        return text

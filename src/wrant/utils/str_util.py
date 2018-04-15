from tqdm import tqdm
import re
from ..constants import DATA_DIR
from . import util


def normalise(text):
    text = text.replace('”', '"').replace('“', '"').replace('’', "'")
    text = text.replace('`', "'").replace('—', '-').replace('…', '...')
    text = text.replace('‘', "'")
    text = re.sub('\n+', '\n', text)
    return text


def get_corpus():
    print('Reading corpus')
    folder = f'{DATA_DIR}/books/'
    texts = []
    for filename in tqdm(util.files(folder)):
        texts.append(normalise(util.read(folder + filename)))
    return texts


def get_by_dep(tokens, dep):
    for tok in tokens:
        if tok.dep_ == dep:
            return tok
    return None

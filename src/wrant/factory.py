from .core import Wrant
from .utils import util
from .constants import DATA_DIR

def create_wrant():
    print('Loading corpus')
    start = util.time.time()
    sents = util.load(f'{DATA_DIR}/sents.pkl')
    print(f'Done in {util.lapsed(start)}')
    return Wrant(sents)

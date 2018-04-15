import spacy
import gc
from collections import defaultdict
from tqdm import tqdm
from ..utils import str_util, util
from ..constants import DATA_DIR, SPACY_MODEL_EN


def process():
    gc.enable()
    nlp = spacy.load(SPACY_MODEL_EN, disable=['ner'])
    texts = str_util.get_corpus()

    verbs = defaultdict(dict)

    for text in tqdm(texts):
        doc = None
        gc.collect()
        doc = nlp(text)
        for tok in doc:
            if tok.pos_ == 'VERB':
                verb_lemma = tok.lemma_
                prt = str_util.get_by_dep(tok.children, 'prt')
                if prt:
                    verb_lemma += '_' + prt.lemma_
                verbs[verb_lemma]
                prep = str_util.get_by_dep(tok.children, 'prep')
                if prep:
                    if prep.lemma_ not in verbs[verb_lemma]:
                        verbs[verb_lemma][prep.lemma_] = 0
                    verbs[verb_lemma][prep.lemma_] += 1

    util.save(verbs, f'{DATA_DIR}/verbs_prep.pkl')

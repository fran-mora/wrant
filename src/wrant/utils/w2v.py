#!/usr/bin/env python3
from gensim.models import word2vec
import sys
import time


sents = word2vec.LineSentence(sys.argv[1])
outfile = sys.argv[2]
start = time.time()
print("Training")
model = word2vec.Word2Vec(sentences=sents, size=200, window=3, workers=30, sg=0, hs=0, negative=10)
print("Training done [" + str(time.time()-start) + "s]")
print("Saving")
model.save(outfile)
print("done.")

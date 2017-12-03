import re
import nltk
import operator
import pickle
import time
import utils.util as util
from nltk_ext import *
from gensim.models import word2vec

class Wrant:
  # _tokens        : list of tokens
  # _text          : plain text
  # _sents         : sentence list, each sentence is a list of tokens
  # _vocab         : vocab set
  # _lowcase_vocab : vocab set lowercased
  # _2_context     : { token : { prev + ' ' + token : cnt} }
  # _3_context     : { token : { prev + ' ' + token + ' ' + next : cnt} }
  # _5_context     : { token : { prev_2 + ' ' + prev + ' ' + token + ' ' + next + ' ' + next_2 : cnt} }
  # _cIndex        : concordance index
  # _doc           : Wrant object of the text to check

  START = '<START>'
  END = '<END>'

  def __init__(self, fileName = '../../data/corpus/corpus_pos_lem.txt', isTokenized=True):
    print('Loading resources...')
    self.lowcase_vocab = None
    start = time.time()
    self.loadCorpus(fileName, isTokenized)
    self.computeContext()
    self.cIndex = ConcordanceIndex(self.tokens, self.lemmas)
    print('done in ' + str(time.time() - start) + ' s')

  @staticmethod
  def load(filename = '../../data/wrant.pkl', inHome=False):
    if inHome:
      filename = '/Users/francesco.moramarco/.wrant/' + filename
    print('Loading pickled object...')
    start = time.time()
    with open(filename, 'rb') as inputFile:
      wrant = pickle.load(inputFile)
      print('done in ' + str(time.time() - start) + ' s')
      return wrant

  @staticmethod
  def save(wrant, filename = '../../datma/wrant.pkl', minimal=False):
    if minimal:
      wrant._2_context = None
      wrant._3_context = None
      wrant._5_context = None
      wrant.rev_2_context = None
      wrant.rev_3_context = None
      wrant.rev_5_context = None
      wrant.text = None
      wrant.sents = None
      wrant.model = None
    with open(filename, 'wb') as output:
      pickle.dump(wrant, output, pickle.HIGHEST_PROTOCOL)

  def w2v(self):
    if not hasattr(self, '_model') or self.model == None:
      self.model = word2vec.Word2Vec.load('../../data/mdels/w2v.model')
    return self.model

  def normalise(self, text):
    return text.replace('`',"'").replace('‘',"'").replace('’',"'") \
               .replace('“','"').replace('”','"')

  def loadCorpus(self, fileName, isTokenized):
    print('Loading corpus')
    text = read(fileName)
    self.sents = []
    self.tokens = []
    self.lemmas = []
    sents = text.split('\n')
    cnt = 0
    tot = len(sents)
    for line in sents:
      if cnt % 10000 == 0:
        print(util.percent(cnt,tot))
      cnt += 1
      sent = []
      for token in line.split(' '):
        pieces = token.split('/')
        tok = pieces[0]
        lemma = pieces[-1]
        sent.append(tok)
        self.tokens.append(tok)
        self.lemmas.append(lemma)
    self.vocab = set()
    for token in self.tokens:
      self.vocab.add(token)

  def computeContext(self):
    print('Computing context')
    _2_context = {}
    _3_context = {}
    _5_context = {}
    rev_2_context = {}
    rev_3_context = {}
    rev_5_context = {}
    for sent in self.sents:
      for i in range(len(sent)):
        prev_2 = sent[i-2] if i > 1 else self.START
        prev   = sent[i-1] if i > 0 else self.START
        next   = sent[i+1] if i < len(sent)-1 else self.END
        next_2 = sent[i+2] if i < len(sent)-2 else self.END
        token = sent[i]
        key_2 = prev + ' ' + token
        key_3 = prev + ' ' + token + ' ' + next
        key_5 = prev_2 + ' ' + prev + ' ' + token + ' ' + next + ' ' + next_2
        key_2_rev = prev
        key_3_rev = prev + ' ' + next
        key_5_rev = prev_2 + ' ' + prev + ' ' + next + ' ' + next_2
        # 2_context
        self.increment(_2_context, token, key_2)
        self.increment(rev_2_context, key_2_rev, token)
        # 3_context
        self.increment(_3_context, token, key_3)
        self.increment(rev_3_context, key_3_rev, token)
        # 5_context
        self.increment(_5_context, token, key_5)
        self.increment(rev_5_context, key_5_rev, token)

    self._2_context = _2_context
    self._3_context = _3_context
    self._5_context = _5_context
    self.rev_2_context = rev_2_context
    self.rev_3_context = rev_3_context
    self.rev_5_context = rev_5_context

  def increment(self, dic, token, key):
    if token not in dic:
      dic[token] = {}
    if key not in dic[token]:
      dic[token][key] = 0
    dic[token][key] += 1


  def concordance(self, words, context = None, context_size = 5, width=75, lines=25):
    self.cIndex.print_concordance(words, context=context, context_size=context_size, width=width, lines=lines)

  def checkDoc(self, text):
    if '_3_context' not in self.__dict__ or self._3_context == None:
        raise("Reload doc")
    sents = self.tokenize(text)
    for sent in sents:
      out = ''
      for i in range(len(sent)):
        prev_2 = sent[i-2] if i > 1 else self.START
        prev   = sent[i-1] if i > 0 else self.START
        next   = sent[i+1] if i < len(sent)-1 else self.END
        next_2 = sent[i+2] if i < len(sent)-2 else self.END
        token  = sent[i]
        out += self.colour(prev_2, prev, token, next, next_2) + ' '
      print(out)

  def check(self, token, prev, next):
    if not token in self._3_context:
      return -1
    key = prev + ' ' + token + ' ' + next
    if not key in self._3_context[token]:
      return 0
    else:
      return self._3_context[token][key]

  def colour(self, prev_2, prev, token, next, next_2):
    if not token in self.vocab:
      return white(token)
    key_5 = prev_2 + ' ' + prev + ' ' + token + ' ' + next + ' ' + next_2
    key_3 = prev + ' ' + token + ' ' + next
    key_2 = prev + ' ' + token
    if key_5 in self._5_context[token]:
      return blue(token)
    if key_3 in self._3_context[token]:
      return green(token)
    if key_2 in self._2_context[token]:
      return yellow(token)
    return red(token)

  def tokenize(self, text):
    text = self.normalise(text)
    sents_list = nltk.sent_tokenize(text)
    sents = []
    for sent in sents_list:
      sents.append(nltk.word_tokenize(sent))
    return sents

  def undefined(self, attr):
    return attr not in self.__dict__ or self.__dict__[attr] == None

  def middle(self, prev, next):
    key = prev + ' ' + next
    if key in self.rev_3_context:
        words = self.rev_3_context[key]
        return sorted(words.items(), key=lambda x:x[1], reverse=True)
    return None

  def best_replacement(self, word, fixes, context):
    if fixes == None:
      return word
#    print("Word: " + word)
#    print("Fixes")
#    print(fixes[:10] if fixes != None else None)
#    print("Most similar")
    most_similar = self.model.most_similar(word,topn=len(self.vocab))
#    print(most_similar[:10])
 #   print("Context: ")
 #   print(context)
 #   print("Predict output word")
 #  print(self._model.predict_output_word(context))

    data = (fixes, most_similar)
    stack = 0
    index = 1

    while index < len(fixes):
      for i in range(index):
        if data[stack][index][0] == data[1-stack][i][0]:
          return data[stack][index][0]
      stack = 1 - stack
      index += 1

    return word

  def fix(self, text):
    if self.undefined('model'):
      self.w2v()
    print("Check result:")
    self.checkDoc(text)

    print("Possible fix:")
    sents = self.tokenize(text)
    for sent in sents:
      fixed = []
      for i in range(len(sent)):
        prev_2 = sent[i-2] if i > 1 else self.START
        prev   = sent[i-1] if i > 0 else self.START
        next   = sent[i+1] if i < len(sent)-1 else self.END
        next_2 = sent[i+2] if i < len(sent)-2 else self.END
        token = sent[i]
        if self.check(token, prev, next) == 0:
          fixes = self.middle(prev, next)
          context = [prev_2, prev, next, next_2]
          context = [x for x in context if x != self.START and x != self.END]
          replacement = self.best_replacement(token, fixes, context)
          fixed.append(blue(replacement) if replacement != token else yellow(token))
        else:
          fixed.append(green(token))
      print(' '.join(fixed))


  def unknown(self, filename = None):
    if filename != None:
      self.loadDoc(filename, isTokenized = False)

    if self.doc == None:
      raise Exception("Pass either text or loadDoc()")
    else:
      if self.lowcase_vocab == None:
        self.lowcase_vocab = set()
        for word in self.vocab:
          self.lowcase_vocab.add(word.lower())

      vocab = self.doc.vocab
      for word in vocab:
        if not word.lower() in self.lowcase_vocab:
          print(word)
          self.doc.concordance(word)

  def word_occurrances(self, text):
    sents = self.tokenize(text)
    vocab = {}
    for sent in sents:
      for token in sent:
        if token not in vocab:
          vocab[token] = 1
        else:
          vocab[token] += 1
        print(f'{token}/{vocab[token]} ', end='')
      print()

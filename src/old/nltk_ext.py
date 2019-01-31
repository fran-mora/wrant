from collections import defaultdict
from util import *
# import nltk


class ConcordanceIndex():
    TOKEN = '§'
    """
    An index that can be used to look up the offset locations at which
    a given word occurs in a document.
    """
    def __init__(self, tokens, tokens_lemma, nlp):
        """
        Construct a new concordance index.

        :param tokens: The document (list of tokens) that this
            concordance index was created from.  This list can be used
            to access the context of a given word occurrence.
        :param key: A function that maps each token to a normalized
            version that will be used as a key in the index.  E.g., if
            you use ``key=lambda s:s.lower()``, then the index will be
            case-insensitive.
        """
        self.nlp = nlp
        self._tokens = tokens
        self._tokens_lemma = tokens_lemma
        """The document (list of tokens) that this concordance index
           was created from."""

        self._offsets = defaultdict(list)
        for index, word in enumerate(tokens):
            word = word.lower()
            self._offsets[word].append(index)

        self._offsets_lemma = defaultdict(list)
        for index, word in enumerate(self._tokens_lemma):
            word = word.lower()
            self._offsets_lemma[word].append(index)

    def tokens(self):
        """
        :rtype: list(str)
        :return: The document that this concordance index was
            created from.
        """
        return self._tokens

    def offsets(self, words, context, context_size):
        """
        :rtype: list(int)
        :return: A list of the offset positions at which the given
            word occurs.  If a key function was specified for the
            index, then given word's key will be looked up.
        """
        word = words[0].lower()
        offsets = list( offset for offset in self._offsets[word] if self.full_match(offset, words, context, context_size) )
        return offsets

    def offsets_lemma(self, words, context, context_size):
        """
        :rtype: list(int)
        :return: A list of the offset positions at which the given
            word occurs.  If a key function was specified for the
            index, then given word's key will be looked up.
        """
        word = words[0].lower()
        offsets = list( offset for offset in self._offsets_lemma[word] if self.full_match_lemma(offset, words, context, context_size) )
        return offsets

    def _match(self, word_corpus, word_text):
        if word_text == ConcordanceIndex.TOKEN:
            return True
        return word_corpus == word_text

    def full_match_lemma(self, offset, words, context, context_size):
        for word in words:
            if offset >= len(self._tokens_lemma) or not self._match(self._tokens_lemma[offset].lower(), word.lower()):
                return False
            offset += 1

        # check context
        if context != None:
            if isinstance(context, str):
                context = [context]
            for word in context:
                if not self._context_match(offset, word, context_size):
                    return False
        return True

    def full_match(self, offset, words, context, context_size):
        for word in words:
            if offset >= len(self._tokens) or not self._match(self._tokens[offset].lower(), word.lower()):
                return False
            offset += 1

        # check context
        if context != None:
            if isinstance(context, str):
                context = [context]
            for word in context:
                if not self._context_match(offset, word, context_size):
                    return False
        return True

    def _context_match(self,offset, word, context_size):
        for i in range(offset - context_size, offset + context_size + 1):
            if i >= 0 and i < len(self._tokens) and word == self._tokens[i]:
                return True
        return False

    def __repr__(self):
        return '<ConcordanceIndex for %d tokens (%d types)>' % (
            len(self._tokens), len(self._offsets))

    def colour_context(self, text, context):
        if context == None:
            return text
        low_text = text.lower()
        for word in context:
            word = ' ' + word + ' '
            if word in low_text:
                index = low_text.index(word)
                text = text[:index] + blue(text[index:index+len(word)]) + text[index+len(word):]
        return text

    def reducePOS(self, pos):
        return 'v' if pos[:2] == 'VB' else 'n'

    def lemmatize(self, words):
        doc = self.nlp(words)
        return [tok.lemma_ for tok in doc]

    def print_concordance(self, words, context=None, lemma=True, context_size=5, width=75, lines=25):
        """
        Print a concordance for ``word`` with the specified context window.

        :param word: The target word
        :type word: str
        :param width: The width of each line, in characters (default=80)
        :type width: int
        :param lines: The number of lines to display (default=25)
        :type lines: int
        """
        # normalise context
        if context is not None:
            context = [self.lemmatize(word) for word in context]

        half_width = (width - len(words) - 2) // 2
        cont = width // 4  # approx number of words of context
        words = self.lemmatize(words)

        size = len(words)
        offsets = self.offsets_lemma(words, context, context_size)
        if offsets:
            lines = min(lines, len(offsets))
            print("Displayed %s of %s matches." % (lines, len(offsets)))
            for i in offsets:
                if lines <= 0:
                    break
                left = (' ' * half_width +
                        ' '.join(self._tokens[i-cont:i]))
                right = ' '.join(self._tokens[i+size:i+cont])
                left = left[-half_width:]
                right = right[:half_width]
                mid = ' '.join(self._tokens[i:i+size])
                print(self.colour_context(left, context), bold(mid), self.colour_context(right, context))
                lines -= 1
        else:
            print("No matches")

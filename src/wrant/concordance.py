from wrant.constants import ANY_TOKEN
from wrant.util import blue, bold


class ConcordanceIndex:
    """
    An index that can be used to look up the offset locations at which
    a given word occurs in a document.
    """
    def __init__(self, corpus, nlp):
        """
        Construct a new concordance index.

        :param tokens: The document (list of tokens) that this
            concordance index was created from.  This list can be used
            to access the context of a given word occurrence.
        """
        self.nlp = nlp
        self._tokens = corpus['tokens']
        self._lemmas = corpus['lemmas']
        self._token_offsets = corpus['token_offsets']
        self._lemma_offsets = corpus['lemma_offsets']
        """The document (list of tokens) that this concordance index
           was created from."""

    def offsets(self, words, context, context_size, lemma=False):
        """
        :rtype: list(int)
        :return: A list of the offset positions at which the first
            word occurs.
        """
        word = words[0].lower()
        offsets = self._lemma_offsets if lemma else self._token_offsets

        return [
            offset for offset in offsets.get(word, [])
            if self.full_match(offset, words, context, context_size, lemma=lemma)
        ]

    @staticmethod
    def match(word_corpus, word_text):
        if word_text == ANY_TOKEN:
            return True
        return word_corpus == word_text

    def full_match(self, offset, words, context, context_size, lemma=False):
        corpus = self._lemmas if lemma else self._tokens
        for i, word in enumerate(words):
            if offset+i >= len(corpus) or not self.match(corpus[offset+i].lower(), word.lower()):
                return False

        # check context
        if context:
            for word in context:
                if not self.context_match(offset, word, context_size, lemma):
                    return False
        return True

    def context_match(self, offset, word, context_size, lemma=False):
        corpus = self._lemmas if lemma else self._tokens

        for i in range(offset - context_size, offset + context_size + 1):
            if 0 <= i < len(corpus) and word == corpus[i]:
                return True
        return False

    @staticmethod
    def colour_context(text, context):
        if context is None:
            return text
        low_text = ' ' + text.lower() + ' '
        for word in context:
            word = ' ' + word + ' '
            if word in low_text:
                index = low_text.index(word)-1
                text = text[:index] + blue(text[index:index+len(word)]) + text[index+len(word):]
        return text

    def get_words(self, text, lemma):
        doc = self.nlp(text)
        if lemma:
            return [tok.lemma_ for tok in doc]
        else:
            return [tok.text for tok in doc]

    def print_concordance(self, text, width=75, lines=25, context=None, lemma=True, context_size=5):
        # normalise context
        if context:
            context = [w for word in context for w in self.get_words(word, lemma)]

        words = self.get_words(text, lemma)

        half_width = (width - len(words) - 2) // 2
        cont = width // 4  # approx number of words of context

        size = len(words)
        offsets = self.offsets(words, context, context_size, lemma=lemma)
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

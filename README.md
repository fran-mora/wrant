# wrant
Writing Assistant

A simple tool to find collocations of words in a given corpus. Useful for finding correct word usages and checking up phrases.

## Clone
```bash
git clone https://github.com/fm2g11/wrant.git
cd wrant
```

## Prerequisites
You need to put some plain text files in `data/books`, ideally books of the same genre to what you want to check.

## Install
```bash
make install  # will install requirements
make build    # will build a corpus based on the books you put in data/books
```

## Run
```python
from wrant import Wrant
wrant = Wrant()
wrant.concordance('stirrup')
wrant.concordance('scratched * back')  # * is a wild character for a single token
wrant.concordance('scratched', context=['back'])  # This means 'back' has to be somewhere around 'scratched'
```

### Arguments
```python
Wrant.concordance(
    text,
    width=100,
    lines=25,
    lemma=True,
    context=[],
    context_size=5
)
```

- **text**: The piece of text to search for. Typically a word or an expression.
- **width**: The number of characters to show for each results.
- **lemma**: Wether to match on lemmas or original tokens. Applies to context too.
- **context**: A list of words that needs to occur near the *text*.
- **context_size**: Number of words (both left and right) from the *text* in which *context* applies to.

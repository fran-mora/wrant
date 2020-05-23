install:
	pip install -e .
	python -m spacy download en_core_web_sm

build:
	mkdir -p data/books/
	python -m wrant.build_corpus


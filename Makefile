install:
	pip3 install -e .

test:
	python3 -m unittest discover -s tests

dev:
	python3 setup.py develop

.PHONY: install test dev

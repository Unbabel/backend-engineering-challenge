install:
	pip3 install -e .

test:
	python3 -m unittest discover -s tests

test-cli:
	cd tests && ./data_tests.sh data

dev:
	python3 setup.py develop

.PHONY: install test dev

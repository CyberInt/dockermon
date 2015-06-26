all:
	$(error please pick a target)

dist:
	python setup.py sdist

test:
	python setup.py nosetests

upload:
	python setup.py sdist upload


.PHONY: all dist test upload

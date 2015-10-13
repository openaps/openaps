
TESTS = $(wildcard openaps/*.py openaps/*/*.py)

test:
	python -m nose
	openaps -h
	# python -m doctest discover
	# do the test dance

ci-test: test
	# do the travis dance


.PHONY: test

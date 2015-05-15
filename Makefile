
TESTS = $(wildcard openaps/*.py openaps/*/*.py)

test:
	openaps -h
	python -m doctest -v ${TESTS}
	# do the test dance

ci-test: test
	# do the travis dance


.PHONY: test


# Some simple testing tasks (sorry, UNIX only).

FLAGS=


flake:
	autoflake -v -v --in-place --recursive --remove-all-unused-imports --ignore-init-module-imports app tests

isort:
	isort app tests

mypy:
	mypy --ignore-missing-imports app tests

black:
	black --line-length 79 --safe --exclude '*.html' --exclude '__pycache__' --verbose app tests

test:
	python3 -m pytest -vvv tests

test_docker:
	docker build --tag=sanic_test --file=Dockerfile_dev . \
	&& docker run sanic_test make test

cov:
	[ -d cov ] || mkdir cov
	python3 -m pytest --cov-config=./config/coveragerc --cov=app --cov-report=html:cov -vvv tests

cov_docker:
	docker build --tag=sanic_test --file=Dockerfile_dev . \
	&& docker run sanic_test make cov

clean:
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]' `
	rm -f `find . -type f -name '*~' `
	rm -f `find . -type f -name '.*~' `
	rm -f `find . -type f -name '@*' `
	rm -f `find . -type f -name '#*#' `
	rm -f `find . -type f -name '*.orig' `
	rm -f `find . -type f -name '*.rej' `
	rm -rf `find . -type d -name '.mypy_cache' `
	rm -rf `find . -type d -name '.pytest_cache' `
	rm -rf .benchmarks
	rm -rf .coverage
	rm -rf .cov
	rm -rf coverage
	rm -rf cov
	rm -rf build
	rm -rf htmlcov
	rm -rf dist

all:
	autoflake -v -v --in-place --recursive --remove-all-unused-imports --ignore-init-module-imports app tests
	isort app tests
	mypy --ignore-missing-imports app tests
	black --line-length 79 --safe --force-exclude 'app/static' --exclude '*.html' --exclude '__pycache__' --verbose app tests
	make test

.PHONY: flake isort black clean test


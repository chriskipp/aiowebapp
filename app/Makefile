# Some simple testing tasks (sorry, UNIX only).

FLAGS=


flake:
	autoflake -v -v --in-place --recursive --remove-all-unused-imports --ignore-init-module-imports app
	autoflake -v -v --in-place --recursive --remove-all-unused-imports --ignore-init-module-imports tests

isort:
	isort app
	isort tests
	mypy --ignore-missing-imports app
	mypy --ignore-missing-imports tests

black:
	black --safe --force-exclude 'app/storage/uploads' --exclude '*.html' --exclude '__pycache__' --verbose app
	black --safe --force-exclude 'app/storage/uploads' --exclude '*.html' --exclude '__pycache__' --verbose tests

test:
	pytest -c config/test.yaml -vvv --disable-warnings tests

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
	rm -rf coverage
	rm -rf build
	rm -rf htmlcov
	rm -rf dist

run-server:
	python3 app/main.py

.PHONY: flake isort black clean test


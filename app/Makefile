# Some simple testing tasks (sorry, UNIX only).

FLAGS=


flake:
	autoflake -v -v --in-place --recursive --remove-all-unused-imports --ignore-init-module-imports app

isort:
	isort --recursive app
	mypy --ignore-missing-imports app

black:
	black --safe --force-exclude 'app/storage/uploads' --exclude '*.html' --exclude '__pycache__' --verbose app

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
	rm -f .coverage
	rm -rf coverage
	rm -rf build
	rm -rf htmlcov
	rm -rf dist

clean_up:
	rm -r .mypy_cache/ .pytest_cache/

run-server:
	python3 -m app

.PHONY: flake isort black clean clean_up  #test


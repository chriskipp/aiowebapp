# Some simple testing tasks (sorry, UNIX only).

FLAGS=


black: clean
	black --line-length 79 --safe .

flake:
	autoflake -v -v --in-place --recursive --remove-all-unused-imports --ignore-init-module-imports .

isort:
	isort .

mypy:
	mypy --install-types .
	mypy --ignore-missing-imports .

lint: black flake isort mypy

#.PHONY: flake isort black clean clean_up  #test

.PHONY: test

test: _virtualenv
	sh -c '. _virtualenv/bin/activate; py.test -vvv tests'

.PHONY: test-all

test-all: _virtualenv
	tox

#.PHONY: upload

#upload: test-all build-dist
#	_virtualenv/bin/twine upload dist/*
#	make clean

.PHONY: build-dist

build-dist: clean
	_virtualenv/bin/pyproject-build

.PHONY: clean

clean:
	rm -rf `find . -name __pycache__`
	rm -rf `find . -type d -name '*.egg-info' `
	rm -f `find . -type f -name '*.py[co]' `
	rm -f `find . -type f -name '*~' `
	rm -f `find . -type f -name '.*~' `
	rm -f `find . -type f -name '@*' `
	rm -f `find . -type f -name '#*#' `
	rm -f `find . -type f -name '*.orig' `
	rm -f `find . -type f -name '*.rej' `
	rm -rf _virtualenv
	rm -rf _requirements.txt
	rm -rf _requirements-dev.txt
	rm -rf .coverage
	rm -rf coverage
	rm -rf build
	rm -rf htmlcov
	rm -rf dist
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf .tox
	rm -f test.sqlite

.PHONY: bootstrap

bootstrap: _virtualenv
	_virtualenv/bin/pip install -e .
ifneq ($(wildcard requirements-dev.txt),)
	_virtualenv/bin/pip install -r requirements.txt
	_virtualenv/bin/pip install -r requirements-dev.txt
endif
	make clean

_virtualenv:
	python3 -m venv _virtualenv
	_virtualenv/bin/pip install --upgrade pip
	_virtualenv/bin/pip install --upgrade setuptools
	_virtualenv/bin/pip install --upgrade wheel
	_virtualenv/bin/pip install --upgrade build twine

update_req: _virtualenv
	sh -c '. _virtualenv/bin/activate; REQILE="requirements-dev.txt"; cat "${REQILE}" | xargs --max-args=1 --delimiter='\n' python3 -m pip install -U; _cat "${REQILE}" | sed -e 's/[<>=]\+.*//' -e 's/^/^/' -e 's/$/[=]/g' > "_${REQILE}"; _python3 -m pip list --format=freeze | grep -f "_${REQILE}" > "${REQILE}"'
	sh -c '. _virtualenv/bin/activate; REQILE="requirements.txt"; cat "${REQILE}" | xargs --max-args=1 --delimiter='\n' python3 -m pip install -U; _cat "${REQILE}" | sed -e 's/[<>=]\+.*//' -e 's/^/^/' -e 's/$/[=]/g' > "_${REQILE}"; _python3 -m pip list --format=freeze | grep -f "_${REQILE}" > "${REQILE}"'



# Some simple testing tasks (sorry, UNIX only).

FLAGS=


flake:
	autoflake -v -v --in-place --recursive --remove-all-unused-imports --ignore-init-module-imports app tests

isort:
	isort app tests

mypy:
	mypy --ignore-missing-imports app tests

black:
	black --line-length 79 --safe --force-exclude 'app/storage/uploads' --exclude '*.html' --exclude '__pycache__' --verbose app tests

test:
	pytest -c config/test.yaml -vvv --disable-warnings --aiohttp-fast tests

test_from_local:
	docker exec -it aiowebapp_aiowebapp_1 make test

localtest:
	pytest -c config/local_test.yaml -vvv --disable-warnings --aiohttp-fast tests

cov:
	#pytest --cov=app --cov-report=shell -c config/test.yaml -vvv --disable-warnings tests

localcov:
	pytest --cov-config=.coveragerc --cov=app --cov-report=html:coverage -c config/local_test.yaml -vvv --disable-warnings --aiohttp-fast tests


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

all:
	autoflake -v -v --in-place --recursive --remove-all-unused-imports --ignore-init-module-imports app tests

	isort app tests
	mypy --ignore-missing-imports app tests

	black --line-length 79 --safe --force-exclude 'app/storage/uploads' --exclude '*.html' --exclude '__pycache__' --verbose app tests

	pytest --cov=app --cov-report=term -c config/local_test.yaml -vvv --disable-warnings --aiohttp-fast tests

.PHONY: flake isort black clean test


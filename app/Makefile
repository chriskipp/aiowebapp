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

test_w_docker_config:
	pytest -c config/test.yaml -vvv --disable-warnings --aiohttp-fast tests

test:
	docker exec -it aiowebapp2_aiowebapp_1 make test_w_docker_config

cov_w_docker_config:
	#pytest --cov-config=.coveragerc --cov=app --cov-report=term -c config/test.yaml -vvv --disable-warnings tests
	pytest --cov-config=.coveragerc --cov=app --cov-report=html:app/storage/coverage -c config/test.yaml -vvv --disable-warnings tests

cov:
	docker exec -it aiowebapp2_aiowebapp_1 make cov_w_docker_config


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

all:
	autoflake -v -v --in-place --recursive --remove-all-unused-imports --ignore-init-module-imports app tests

	isort app tests
	mypy --ignore-missing-imports app tests

	black --line-length 79 --safe --force-exclude 'app/storage/uploads' --exclude '*.html' --exclude '__pycache__' --verbose app tests

	make test

.PHONY: flake isort black clean test


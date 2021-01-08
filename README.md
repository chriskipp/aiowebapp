# aiowebapp

Batteries included fully asyncronous (aiohttp based) web application. The web server comes together with a (postgres) database backend, a redis server and a (nginx) reverse proxy. Everything is packed for ease use as a little (docker-compose based) docker swarm.

## Features

This repository is mainly ment as a skelleton for aiohttp based webapps, including certain features like login or (http/https) nginx-reverse-proxy out-of-the-box. Beside this there are a hand full of tools including a database manager a redis based search engine or a nominatim based search engine for geographic entities as examples on how to use this skelleton. Further features include:

### Container based features
- [aiohttp](https://github.com/aio-libs/aiohttp) is used as a asyncronous web server
- [nginx](http://nginx.org/) as a reverse proxy (including support for https using self-signed certificates)
- [postgres](https://www.postgresql.org/) as a relational database
- [redis](https://redis.io/) as in memory database
- [redisearch](https://github.com/RediSearch/RediSearch) as redis based search engine with autocompletion
- [redisJSON](https://github.com/RedisJSON/RedisJSON) JSON support for redis
- Extra importer container (not belonging to the webapp itself) to fill the application's redis and postgres backends with some example data from the web to make the provided example tools work

### Web app features
- [aiohttp-session](https://github.com/aio-libs/aiohttp-session) session and login support
- [trafaret-config](https://github.com/tailhook/trafaret-config) to safely parse config files
- [aiopg.sa](https://github.com/aio-libs/aiopg) as async database adapter to handle user login with SQLAlchemy support
- [aiohttp-jinja2](https://github.com/aio-libs/aiohttp-jinja2) templating system
- file up- and download to the server

### Featuers to increase speed
- [uvloop](https://github.com/MagicStack/uvloop) to generally speed up the web application
- [orjson](https://github.com/ijl/orjson) to speed up JSON serialisation
- [asyncpg](https://github.com/MagicStack/asyncpg) ultra fast async database interface to handle raw SQL queries
- [cchardet](https://github.com/PyYoshi/cChardet) and [aiodns](https://github.com/saghul/aiodns) as they are officially recommended to generally speed up aiohttp based applications

### Web app tools/Example Pages
- [leaflet Map](https://github.com/Leaflet/Leaflet) interactive Map
- [ACE Editor](https://ace.c9.io/) high performance code editor with support for over 120 languages
- [SlickGrid](https://github.com/6pac/SlickGrid) web based grid with build in support for (Multi Column) Sorting, Data Type Detection, Autosize of Columns, (Drag & Drop based) Grouping, ...
- [Redis based Search Engine](https://github.com/RediSearch/RediSearch) with XHR based autocompletion (To generate a example index of locally installed man pages see the scripts section)
- [GeoSearch](https://nominatim.org/release-docs/develop/api/Overview) using the Nominatim API as back- and Leaflet's GeoJSON support as frontend

### Development and Testing
- almost 100% test coverage using [pytest](https://github.com/pytest-dev/pytest) and [pytest-cov](https://github.com/pytest-dev/pytest-cov)
- [aiohttp-debugtoolbar](https://github.com/aio-libs/aiohttp-debugtoolbar) including two extra pannels to analyse postgres and redis queries
- automatic linting ([autoflake](https://github.com/myint/autoflake)) and code formatting ([black](https://github.com/psf/black), [isort](https://github.com/PyCQA/isort))

## Running the Application

### Using HTTP

The only required software packages to start this application are docker/docker-compose. After cloning this repository  this repository run the following command to start up the application:

```
$ docker-compose up
```

### Using HTTPS

To be able to use SSL Encryption you will need a certificate/key pair. To generate your own self-signed certificate run the provided shell script ```create_certificate.sh``` (you will need openssl to generate your own certificates):

```
$ ./create_certificate.sh
```

Once you have your certificate the setup process is similar as described under HTTP except that docker-compose is executed with the option ```--file docker-compose_ssl.yml```:

To start the web application:

```
$ docker-compose --file docker-compose_ssl.yml up
```

## Providing example data to the application

The above commands will run the web application, the database backend, the redis server including redisearch and RedisJSON plugins and the nginx reverse proxy. To make use of the build in redis based search engine as well as to provide some example data to the database you can run the scripts in the scripts directory. These will provide the following data:

- [create_man_index.sh](./scripts/create_man_index.sh) Generates a search index of the manual pages installed on the (LOCAL!) system. This means you need to have some manual pages installed in the directory /usr/share/man[18].
- [import_rest_countries.sh](./scripts/import_rest_countries.sh) This will import country related data from the [Restcountries API](https://restcountries.eu/rest/v2/all)
- [import_js_libraries.sh](./scripts/import_js_libraries.sh) This will import information on all javascript libraries availible on [CDNJS](https://api.cdnjs.com/libraries/) into the database
- [import_pypi_pkgs.sh](./scripts/import_pypi_pkgs.sh) This will import information about all python packages used in this project from the [Python Package Index](https://pypi.org/pypi/) to the database
- [import_corona_stats.py](./scripts/import_corona_stats.py) This will import a daily statistics of all countries about the [Corona Virus Pandemic](https://pomber.github.io/covid19/timeseries.json)

**Note:** Since the provided tests also test the functionality of the included search engine and its autocompletion some example index has to be created to guarantee the successful passing of the related tests!

Instead of installing the nessesary programs locally you can also run the docker container provided by the Dockerfile in the scripts directory:

```
docker build -t aiowebapp_importer scripts && docker run --network=host aiowebapp_importer
```

Please note, that this container is only ment for providing the example data an is not part of the actual docker swarm used to run the app itself.

## Running Tests

After successful startup of the web application you might want to run the provided tests to make sure all features are working properly. By default testing is automatically achieved from within the running docker container. You can initiate testing by using the ```Makefile``` in the ```app``` directory:

```
$ make test
```

# aiowebapp

Various own projects that came about in the form of individual aiohttp based web applications and are now being compiled here in the form of a docker swarm in a repository as many of the applications complement.

## Features

This repository is mainly ment as a skelleton for a aiohttp based app, including certain features like login or nginx-reverse-proxy out-of-the-box. Beside this there are a hand full of sub applications including a database manager and search engines as examples on how to use this skelleton. Features include:

### Container based features
- [aiohttp](https://github.com/aio-libs/aiohttp) is used as a asyncronous web server
- [nginx](http://nginx.org/) as a reverse proxy (including support for https using self-signed certificates)
- [postgres](https://www.postgresql.org/) as a relational database
- [redis](https://redis.io/) as in memory database

### Web app features
- [uvloop](https://github.com/MagicStack/uvloop) to generally speed up the web application
- [aiohttp-session](https://github.com/aio-libs/aiohttp-session) session and login support
- [orjson](https://github.com/ijl/orjson) to speed up JSON serialisation
- [trafaret-config](https://github.com/tailhook/trafaret-config) to safely parse config files
- [asyncpg.sa](https://github.com/aio-libs/aiopg) as async database adapter to support user login

## Dependencies and Installation

### Using HTTP

The only required Software packages to start this application are docker and docker-compose. After cloning this repository  this repository run the following command to start up the application:

```
$ docker-compose up
```

### Using HTTPS

To be able to use SSL Encryption you will need a certificate/certificate_key pair. To generate your own self-signed certificate run the provided shell script ```create_certificate.sh``` (you will need openssl):

```
$ ./create_certificate.sh
```

Once you have your certificate the setup process is similar as described under HTTP except that docker-compose is executed with the option ```--file docker-compose_ssl.yml```:

To start the web application:

```
$ docker-compose --file docker-compose_ssl.yml up
```

## Running Tests

After successful startup of the web application you might want to run the provided tests to make sure all features are working properly. By default testing is automatically achieved from within the running docker container. You can initiate testing by using the ```Makefile``` in the ```app``` directory:

```
$ make test
```



## Included Components



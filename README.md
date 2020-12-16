# aiowebapp

Various own projects that came about in the form of individual aiohttp based web applications and are now being compiled here in the form of a docker swarm in a repository as many of the applications complement.

## Dependencies and Installation

### Using HTTP

The only required Software packages to start this application are docker and docker-compose. After cloning this repository  this repository run the following command to start up the nginx, redis and postgres container as well as initialize the database schema (only if it is postgres first startup):

```
$ docker-compose up -d postgres redis nginx
```

When the above services are up and running start the web app itself by running:

```
$ docker-compose up aiowebapp
```

### Using HTTPS

To be able to use SSL Encryption you will need a certificate/certificate_key pair. To generate your own self-signed certificate run the provided shell script ```create_certificate.sh``` (you will need openssl):

```
$ ./create_certificate.sh
```

Once you have your certificate the setup process is similar as described under HTTP except that docker-compose is executed with the option ```--file docker-compose_ssl.yml```:

To initialize and startup the nessesary services:
```
$ docker-compose up --file docker-compose_ssl.yml -d postgres redis nginx
```

To start the web application:

```
$ docker-compose --file docker-compose_ssl.yml up aiowebapp
```

## Running Tests

After successful startup of the web application you might want to run the provided tests to make sure all features are working properly. By default testing is automatically achieved from within the running docker container. You can initiate testing by using the ```Makefile``` in the ```app``` directory:

```
$ make test
```



## Included Components



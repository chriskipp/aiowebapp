#!/bin/zsh

sqlthemall --database "postgresql://api:apipw@localhost:5432/storage" --url "https://restcountries.eu/rest/v2/all" --root-table "countries"

#!/bin/zsh

sqlthemall --database "postgresql://crawler:crawler@localhost:5432/crawler" --url "https://restcountries.eu/rest/v2/all" --root-table "countries"

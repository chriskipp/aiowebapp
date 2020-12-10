#!/bin/sh

# To run app in docker container use:
python3 -m app.main -c config/dev.yaml
# adev runserver --livereload --host 0.0.0.0 --port 8080 app

# To run app locally use:
# python3 -m app.main -c config/local_dev.yaml

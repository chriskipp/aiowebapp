FROM python:3.9.4

WORKDIR /src/importer
RUN apt-get update && apt-get -y upgrade && apt-get install -y git man-db manpages build-essential zsh redis bc jq
RUN python3 -m pip install psycopg2 psycopg2-binary html2text
RUN git clone 'https://github.com/chriskipp/sqlthemall' && cd sqlthemall && python3 setup.py install && cd .. && rm -r ./sqlthemall

ADD . .
RUN ./install_parallel.sh
RUN env_parallel --install
#CMD ./create_man_index.sh; ./import_corona_stats.py; ./import_js_libraries.sh; ./import_rest_countries.sh; ./import_pypi_pkgs.sh
CMD ./create_man_index.sh

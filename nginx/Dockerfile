FROM nginx:1.21.3-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx/* /etc/nginx/
RUN ln -s /usr/lib/nginx/modules /etc/nginx/modules


COPY snippets /etc/nginx/snippets
COPY ssl /etc/ssl
COPY dhparam.pem /etc/nginx/

COPY app.conf /etc/nginx/conf.d/app.conf


FROM nginx:1.21.3-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx /etc/nginx
COPY ssl /etc/ssl
RUN ln -s /usr/lib/nginx/modules /etc/nginx/modules

COPY server/app.conf /etc/nginx/conf.d/app.conf

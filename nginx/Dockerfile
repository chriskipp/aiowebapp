FROM nginx:1.21.3-alpine

COPY nginx /etc/nginx
RUN ln -s /etc/nginx/sites-availible/default /etc/nginx/sites-enabled/default
RUN ln -s /usr/lib/nginx/modules /etc/nginx/modules

#RUN rm /etc/nginx/conf.d/default.conf
#RUN rm /etc/nginx/sites-availible/
COPY app.conf /etc/nginx/conf.d/app.conf


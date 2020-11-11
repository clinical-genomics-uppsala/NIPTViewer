FROM nginx:1.19.0-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY ./dockerfiles/nginx.prod.conf /etc/nginx/conf.d/nginx.conf

RUN mkdir -p /etc/ssl/certs/
COPY ./SSL/nginx-selfsigned.crt /etc/ssl/certs/nginx-selfsigned.crt

RUN mkdir -p /etc/ssl/private/
COPY ./SSL/nginx-selfsigned.key /etc/ssl/private/nginx-selfsigned.key

COPY ./SSL/dhparam.pem /etc/nginx/dhparam.pem

RUN mkdir -p /etc/nginx/snippet/
COPY dockerfiles/ssl-params.conf /etc/nginx/snippet/ssl-params.conf
COPY dockerfiles/self-signed.conf /etc/nginx/snippet/self-signed.conf

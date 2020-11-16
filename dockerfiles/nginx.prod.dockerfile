FROM nginx:1.19.0-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY ./dockerfiles/nginx.prod.conf /etc/nginx/conf.d/nginx.conf

COPY ./SSL/dhparam.pem /etc/nginx/dhparam.pem

RUN mkdir -p /etc/nginx/snippet/
COPY dockerfiles/ssl-params.conf /etc/nginx/snippet/ssl-params.conf
COPY dockerfiles/self-signed.conf /etc/nginx/snippet/self-signed.conf

RUN mkdir -p /etc/letsencrypt/live/cgu.igp.uu.se

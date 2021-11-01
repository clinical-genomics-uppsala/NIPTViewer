FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf
COPY ./dockerfiles/nginx.prod.conf /etc/nginx/conf.d/nginx.conf

#COPY ./SSL/dhparam.pem /etc/nginx/dhparam.pem

RUN mkdir -p /etc/certs/
COPY ./certs/public.crt /etc/certs/
COPY ./certs/private.rsa /etc/certs/
#COPY dockerfiles/ssl-params.conf /etc/nginx/snippet/ssl-params.conf
#COPY dockerfiles/self-signed.conf /etc/nginx/snippet/self-signed.conf

#RUN mkdir -p /etc/letsencrypt/live/cgu.igp.uu.se

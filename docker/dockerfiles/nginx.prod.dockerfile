FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf
COPY ./docker/dockerfiles/nginx.prod.conf /etc/nginx/conf.d/nginx.conf

RUN mkdir -p /etc/certs/
COPY ./certs/public.crt /etc/certs/
COPY ./certs/private.rsa /etc/certs/

FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf
COPY ./docker/prod/nginx.prod.conf /etc/nginx/conf.d/nginx.conf
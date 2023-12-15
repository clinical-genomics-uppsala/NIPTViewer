FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf
COPY ./docker/dev/nginx.dev.conf /etc/nginx/conf.d/nginx.conf

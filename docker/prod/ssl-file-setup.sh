#!/bin/bash


mkdir SSL;
openssl req -x509 -nodes -days 1000 -newkey rsa:4096 -keyout ./SSL/nginx-selfsigned.key -out ./SSL/nginx-selfsigned.crt
#openssl dhparam -out SSL/dhparam.pem 4096;
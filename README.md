docker-compose -f docker-compose-production.yaml exec web python3 manage.py collectstatic --noinput --clear
docker-compose -f docker-compose-production.yaml exec web python3 manage.py collectstatic --noinput --clear

docker-compose -f docker-compose-production.yaml exec web python3 manage.py loaddata index
docker-compose -f docker-compose-production.yaml exec web python3 manage.py loaddata sample_types
docker-compose -f docker-compose-production.yaml exec web python3 manage.py createsuperuser

sudo openssl req -x509 -nodes -days 1000 -newkey rsa:2048 -keyout ./SSL/nginx-selfsigned.key -out ./SSL/nginx-selfsigned.crt

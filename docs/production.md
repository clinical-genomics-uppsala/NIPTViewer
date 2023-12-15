# Production
For production usage it's recommended that [https](https://en.wikipedia.org/wiki/HTTPS) is used, this require signed certificates preferably provided by your organization. If not, there are some alternatives:

 - [letsencrypt](https://letsencrypt.org/)
 - self signed certifcates

Self signed certificates can be generated using openssl. **Note**: to use self signed certificates you will have tweak your web browser to accept the certificate.

## Nginx


### Domain

** Regular docker **  
Substituted localhost in `docker/prod/nginx.prod.dockerfile` with your domain, before building the nginx container.

** Podman/kuberenets**  
Substituted localhost in `kuberenets/nginx/nginx.conf` with your domain, before building the nginx container.


### Self-signed certifcates

Self-signed certificates can easily be generated using openssl

** Regular docker **
```bash
# Create self signed certificates if signed certificate doesn't exist
cd docker/prod
bash ssl-file-setup.sh
```

** Podman/Kuberenets **
Self signed certificates can easily be generated.
```bash
# Create self signed certificates if signed certificate doesn't exist
cd kuberenetes/nginx
bash ssl-file-setup.sh
```

### Build

** Regular docker **
```bash
docker build -f docker/prod/nginx.dockerfile --tag smeds84/niptviewernginx:1.0.0 .
```

** Podman/Kuberenets **
```bash
# Docker
docker build -f kubernetes/nginx/nginx.dockerfile --tag smeds84/niptviewernginx:1.0.0 .

# Podman
podman build -f kubernetes/nginx/nginx.dockerfile --tag smeds84/niptviewernginx:1.0.0 .
```

## Docker

### Config
Make the following updates before deploying NIPTviewer in production using regular docker:

** Certificates **  
update certifcates path (key and crt) in docker-compose-production.yaml

```yaml
services:
  nipt-nginx-service:
    volumes:
      - ./docker/prod/SSL/nginx-selfsigned.crt:/etc/certs/public.crt
      - ./docker/prod/SSL/nginx-selfsigned.key:/etc/certs/private.key
```  

** NIPTviewer **  
Update `docker/prod/.env_web` to change NIPTviewer settings. As minimum the [SECRET_KEY](https://docs.djangoproject.com/en/dev/ref/settings/#secret-key) should be replaced with a uniq random string. In this file it's also possible to change database settings.

### Deploy and setup
```bash
# Build and spin up containers
VERSION="{NIPT_VERSION}" docker-compose -f docker-compose-production.yaml up --build -d

# Setup database and import initial data
# Migrate, apply data models
docker exec -it {NIPT_WEB_CONTAINER_NAME_OR_ID} python3 manage.py migrate

# Load fixtures
docker exec -it {NIPT_WEB_CONTAINER_NAME_OR_ID} python3 manage.py loaddata index
docker exec -it {NIPT_WEB_CONTAINER_NAME_OR_ID} python3 manage.py loaddata sample_types

# Create admin user
docker exec -it {NIPT_WEB_CONTAINER_NAME_OR_ID} python3 manage.py createsuperuser

# Setup files
# Collect staticfiles, image, js and css
docker exec -it {NIPT_WEB_CONTAINER_NAME_OR_ID} python3 manage.py collectstatic
```

The service should now be avaible at https://localhost:443

## Podman/kubernetes
** Note ** the deployment has only been tested using podman

### Config
Make the following updates before deploying NIPTviewer in production using podman/kuberenetes.

** certificates **  
update certifcates part (crt and key) in kuberenets/kube_production.yaml

```yaml
spec:
  volumes:
    - name: crt_file
      hostpath:
        path: nginx/SSL/nginx-selfsigned.crt
    - name: key_file
      hostpath:
        path: nginx/SSL/nginx-selfsigned.key
```  

** domain settings **  
Substituted localhost in `docker/prod/nginx.prod.dockerfile` with your domain, before building the nginx container.

** NIPTviewer **  
To update NIPTviewer settings `./docker/prod/.env_web` must updated. As minimum the [SECRET_KEY](https://docs.djangoproject.com/en/dev/ref/settings/#secret-key) should be replaced with a uniq random string. In this file it's also possible to change database settings.


### Deploy container
```bash
# Deploy containers
podman play kube kube_production.yaml

# Setup database and import initial data
# Migrate, apply data models
podman exec -it {NIPT_WEB_SERVICE_ID} python3 manage.py migrate

# Load fixtures
podman exec -it {NIPT_WEB_SERVICE_ID} python3 manage.py loaddata index
podman exec -it {NIPT_WEB_SERVICE_ID} python3 manage.py loaddata sample_types

# Setup files
# Collect staticfiles, image, js and css
podman exec -it {NIPT_WEB_SERVICE_ID} python3 manage.py collectstatic

# Create admin user
docker exec -it {NIPT_WEB_SERVICE_ID} python3 manage.py createsuperuser

```

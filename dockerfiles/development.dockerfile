# pull official base image
FROM python:3.8-slim

ENV LANG C.UTF-8
ENV TZ=Europe/Stockholm
ENV DEBIAN_FRONTEND=noninteractive
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get install -y git

ENV APP_HOME=/usr/src/app
RUN mkdir -p $APP_HOME

# set work directory
WORKDIR $APP_HOME

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

# install dependencies
RUN pip install --upgrade pip
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.prod.txt

RUN adduser app

# install dependencies
RUN apt update && apt install netcat libpq-dev wkhtmltopdf vim -y
RUN pip install --no-cache /wheels/*

COPY ./dockerfiles/entrypoint-dev.sh /entrypoint.sh

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

WORKDIR $APP_HOME
# change to the app user
USER app
ENV DEBUG=1
ENTRYPOINT ["/entrypoint.sh"]

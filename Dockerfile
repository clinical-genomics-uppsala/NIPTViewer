ARG VERSION="master"

###########
# BUILDER #
###########

# pull official base image
FROM python:3.8-slim as builder

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip

COPY ./requirements.prod.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.prod.txt
 -r requirements.prod.txt

# pull official base image
FROM ubuntu:20.04

LABEL maintainer="patrik.smeds@scilifelab.uu.se"
LABEL version=$VERSION

ENV LANG C.UTF-8
ENV TZ=Europe/Stockholm
ENV DEBIAN_FRONTEND=noninteractive
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN mkdir -p /home/app

RUN adduser -rm -d /home/app -s /bin/bash -g root -G sudo app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME/staticfiles
WORKDIR $APP_HOME

# install dependencies
RUN apt update && apt install curl gnupg2 -y
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list | tee /etc/apt/sources.list.d/msprod.list
RUN apt update && ACCEPT_EULA=Y  apt install unixodbc-dev build-essential libpq-dev wkhtmltopdf vim wget msodbcsql17 -y
RUN apt update && apt install python3-pip -y
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.prod.txt .
RUN pip install --no-cache /wheels/*

COPY ./dockerfiles/entrypoint.sh /home/app/

COPY ./niptviewer $APP_HOME
RUN apt purge build-essential unixodbc-dev -y
# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app

ENTRYPOINT ["/home/app/entrypoint.sh"]

CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "niptviewer.wsgi:application"]rkers", "3", "niptviewer.wsgi:application"]

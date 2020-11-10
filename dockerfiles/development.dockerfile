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
#RUN pip install flake8


# copy project
COPY . .
#RUN flake8 --ignore=E501,F401 .

COPY ./requirements.prod.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.prod.txt

#########
# FINAL #
#########

# pull official base image
FROM python:3.8-slim

ENV LANG C.UTF-8
ENV TZ=Europe/Stockholm
ENV DEBIAN_FRONTEND=noninteractive
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN mkdir -p /home/app

#RUN addgroup --disabled-password --gecos "" app
RUN adduser app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
#RUN mkdir $APP_HOME/staticfiles
WORKDIR $APP_HOME

# install dependencies
RUN apt update && apt install netcat libpq-dev wkhtmltopdf vim -y
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.prod.txt .
RUN pip install --no-cache /wheels/*

COPY ./dockerfiles/entrypoint.sh .

COPY ./niptviewer $APP_HOME

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app

ENTRYPOINT ["/home/app/web/entrypoint.sh"]

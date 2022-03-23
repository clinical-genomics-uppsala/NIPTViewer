FROM ubuntu:20.04
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
LABEL maintainer="patrik.smeds@scilifelab.uu.se"
LABEL version=$VERSION

ARG VERSION="master"

ENV LANG C.UTF-8
ENV TZ=Europe/Stockholm

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone

ENV DEBIAN_FRONTEND=noninteractive

RUN mkdir -p /home/app && adduser --system  --home /home/app --shell /bin/bash --group app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir -p $APP_HOME/staticfiles
WORKDIR $APP_HOME

# install dependencies
RUN apt-get update \
    && apt-get install --no-install-recommends gnupg2=2.2.19-3ubuntu2.1 \
                                               curl=7.68.0-1ubuntu2.7 \
                                               build-essential=12.8ubuntu1.1 \
                                               libpq-dev=12.9-0ubuntu0.20.04.1 \
                                               wkhtmltopdf=0.12.5-1build1 \
                                               vim=2:8.1.2269-1ubuntu5.7 \
                                               python3-dev=3.8.2-0ubuntu2 \
                                               python3-pip=20.0.2-5ubuntu1.6 \
                                               wget=1.20.3-1ubuntu2 -y \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list | tee /etc/apt/sources.list.d/msprod.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install --no-install-recommends msodbcsql17=17.9.1.1-1 unixodbc-dev=2.3.7 -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/


COPY pyproject.toml /pyproject.toml

COPY ./docker/dockerfiles/entrypoint.sh /home/app/

COPY ./niptviewer $APP_HOME
RUN sed -E "s/[0-9]+\.[0-9]+\.[0-9]+/$VERSION/" -i $APP_HOME/niptviewer/__init__.py

COPY requirements.prod.txt $APP_HOME
RUN pip install --no-cache-dir -r $APP_HOME/requirements.prod.txt  \
    && apt-get purge build-essential unixodbc-dev -y \
    && chown -R app:app $APP_HOME

# change to the app user
USER app

ENTRYPOINT ["/home/app/entrypoint.sh"]

CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "niptviewer.wsgi:application"]

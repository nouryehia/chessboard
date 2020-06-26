###########
# BUILDER #
###########

# pull base image
FROM python:3.8.1-slim-buster as builder

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Need this for our entrypoint
RUN apt-get update && apt-get install -y --no-install-recommends gcc

# lint
RUN pip install --upgrade pip
COPY . /usr/src/app

# build deps
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

#########
# FINAL #
#########

# pull base image
FROM python:3.8.1-slim-buster

# create directory for the app user
RUN mkdir -p /home/app

# create the user
RUN adduser --system --group app

# create appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/chessboard
WORKDIR $APP_HOME

# install deps
RUN apt-get update && apt-get install -y --no-install-recommends netcat
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

# copy the project
COPY . $APP_HOME

# change the owner of the files
RUN chown -R app:app $APP_HOME

# change user
USER app

# start it up
ENTRYPOINT ["/home/app/chessboard/entrypoint.sh"]


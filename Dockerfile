# pull base image
FROM python:3.8.1-slim-buster

# set working directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# gotta show the port
EXPOSE 5000

# Need this for our entrypoint
RUN apt-get update && apt-get install -y netcat

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . /usr/src/app

# run the entrypoint
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]


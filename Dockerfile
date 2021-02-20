FROM python:3.9
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
RUN mkdir /app/staticfiles
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/
COPY ./deploy/docker-entrypoint.sh ./docker-entrypoint.sh
FROM python:3.10

ARG USER_ID=2000
ARG GROUP_ID=2000


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install \
    && python -m pip install --upgrade pip


WORKDIR /app

COPY docker/requirements.txt /app/
RUN pip install -r requirements.txt
COPY docker /app/


USER test

ENTRYPOINT ["sh","/app/docker/server_run.sh"]

#RUN ["docker/server_run.sh"]






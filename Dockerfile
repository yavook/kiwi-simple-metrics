FROM python:3.11-alpine

ENV \
    PYTHONUNBUFFERED=1

COPY . /usr/src/app

RUN set -ex; \
    # buildtime deps
    apk add --no-cache \
        --virtual .build-deps \
        build-base \
        gcc \
        linux-headers \
    ;

RUN set -ex; \
    pip3 --no-cache-dir install /usr/src/app

ENTRYPOINT ["kiwi-simple-metrics"]
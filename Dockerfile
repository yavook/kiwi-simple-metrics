FROM python:3.11-alpine

ENV \
    PYTHONUNBUFFERED=1

# copy app source
COPY . /usr/src/app

RUN set -ex; \
    # install buildtime deps
    apk add --no-cache \
        --virtual .build-deps \
        build-base \
        gcc \
        linux-headers \
    ; \
    # install app
    pip3 --no-cache-dir install /usr/src/app; \
    # remove buildtime deps
    apk del --no-cache \
        .build-deps \
    ;

ENTRYPOINT ["kiwi-simple-metrics"]
FROM python:3.8.6-alpine3.12

RUN apk update && \
    apk add --no-cache \
        build-base \
        libffi-dev \
        zlib-dev \
        py-pip \
        jpeg-dev \
        postgresql-dev

ENV LIBRARY_PATH=/lib:/usr/lib

RUN pip install --upgrade pip

RUN pip install pipenv

COPY bricks/Pipfile bricks/Pipfile.lock ./

RUN pip install --pre gql[aiohttp]

RUN pip install pandas

RUN pip install -U matplotlib

RUN pipenv lock

RUN pipenv install --system --deploy

WORKDIR /usr/src/api

EXPOSE 8000

# DEV
CMD ["adev", "runserver", "./bricks.py"]

# PROD
# CMD ["gunicorn", "-c", "gunicorn.py", "bricks:app"]

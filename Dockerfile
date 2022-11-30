FROM python:3.7.13-alpine3.16

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

EXPOSE 3030

CMD ["python3", "app.py"]
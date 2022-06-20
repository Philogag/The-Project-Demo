
FROM python:3.9.11-alpine3.15

MAINTAINER "haoran.yu"
WORKDIR /deploy

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple gunicorn gevent

COPY requirements.txt requirements.txt

RUN \
 sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories && \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc g++ musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir && \
 apk --purge del .build-deps

# fix flask_script
RUN \
 sed -i s/flask._compat/flask_script._compat/g /usr/local/lib/python3.9/site-packages/flask_script/__init__.py

EXPOSE 8080

WORKDIR /deploy/src

CMD gunicorn -c gunicorn.py app_entry:app
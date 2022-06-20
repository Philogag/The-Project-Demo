
FROM python:3.9-buster

MAINTAINER "haoran.yu"

WORKDIR /deploy/src

COPY requirements.txt requirements.txt
RUN apt-get install -y libpq-dev && \
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir

COPY backend backend

EXPOSE 8080

# ENTRYPOINT ["/bin/bash", "-c"]
CMD ["gunicorn","-c","backend/gunicorn.py","backend.app_entry:flask_app"]
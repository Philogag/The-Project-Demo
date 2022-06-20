#!/bin/bash

docker run -it \
    -v $PWD/../backend:/deploy/src/backend \
    -v $PWD/../alembic.ini:/deploy/src/alembic.ini \
    -v $PWD/../alembic:/deploy/src/alembic \
    --network=deploy_default \
    -e FLASK_CONFIG_TOML="./backend/app.production.toml" \
    deploy_backend \
    python backend/script.py $@
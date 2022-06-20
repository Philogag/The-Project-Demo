#!/bin/bash

docker run -it --rm \
    -v $PWD/../backend:/deploy/src/backend \
    -v $PWD/../alembic.ini:/deploy/src/alembic.ini \
    -v $PWD/../alembic:/deploy/src/alembic \
    --network=deploy_default \
    -e FLASK_CONFIG_TOML="./backend/app.production.toml" \
    sport_meeting_backend \
    alembic $@
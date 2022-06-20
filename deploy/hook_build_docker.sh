#!/bin/bash


docker build . -f ./deploy/dockerfile/backend.run.Dockerfile -t sport_meeting_backend
docker container prune -f
docker image prune -f
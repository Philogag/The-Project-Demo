#!/bin/bash

# please run at the root of project-folder
workdir=$PWD

git pull
## build frontend
cd $workdir/frontend/desktop
npm run build


## restart backend
# update database struct

# cd $workdir
# ./deploy/hook_build_docker.sh

cd $workdir/deploy
docker-compose up -d

docker restart sport_meeting_backend

echo Done.

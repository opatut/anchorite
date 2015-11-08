#!/bin/bash

set -e

VER=$1
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)

cd client
npm run build
cd .. 

git checkout -B deploy
git add server/anchorite/static/* -f
git commit -m "Deploy $VER"
git push --force origin deploy

git checkout $CURRENT_BRANCH

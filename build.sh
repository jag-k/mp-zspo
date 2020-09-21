#!/bin/bash

echo
echo "======= Go to master"
git checkout master
git pull origin master

echo
echo "======= Init build"
git push origin --delete build
git checkout -b build

echo
echo "======= Building"
npm run build
rm -rf node_modules .gitignore venv src
git add .
git commit -m "Build at $(date '+%Y-%m-%d_%H:%M:%S')"
git push origin build

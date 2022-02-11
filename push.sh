#!/bin/bash
set -e -u

git submodule update --init
git submodule update --remote

git add -A
git commit -m "${1}"
git push 

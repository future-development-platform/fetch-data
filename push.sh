#!/bin/bash
work_dir=$(dirname $(realpath -- $0))

cd "${work_dir}"
git submodule update --init
git submodule update --remote
cd "${work_dir}/data" && "${work_dir}/data/git-push.sh"

cd "${work_dir}"
git submodule update --init
git submodule update --remote

git add -A
git commit -m "${1}"
git push 

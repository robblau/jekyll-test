#!/bin/bash

# make sure we are inside docker world
if [ ! -f /.dockerenv ]; then
    echo "You need to run this script from inside a docker container";
    exit 1
fi

ROOT_FOLDER=/app
BUILD_FOLDER=${ROOT_FOLDER}/_build


# exit on error
set -e

echo "------------------------------------------------------"
echo "doc build process starting"
echo `python --version`
echo `ruby --version`
echo "------------------------------------------------------"

echo "cleaning out build location"
rm -rf ${ROOT_FOLDER}/_build

echo "creating build location"
mkdir ${BUILD_FOLDER}
mkdir ${BUILD_FOLDER}/markdown_src

echo "copying markdown docs scaffold into build locatio"
cp -r ${ROOT_FOLDER}/docs/* ${BUILD_FOLDER}/markdown_src

echo "running python script compile"
#python ${ROOT_FOLDER}/scripts_docker/generate_sphinx_markdown.py

git clone --depth 1 https://github.com/shotgunsoftware/tk-core.git ${BUILD_FOLDER}/git/tk-core
export PYTHONPATH=$PYTHONPATH:${BUILD_FOLDER}/git/tk-core/python

sphinx-build -h

sphinx-build -b markdown -c ${ROOT_FOLDER}/sphinx -D project='foo' -D release='bar' -D version='0.0.0' ${BUILD_FOLDER}/git/tk-core/docs ${BUILD_FOLDER}/sphinx/tk-core


echo "building jekyll site"

bundle exec jekyll build --help

JEKYLL_ENV=production bundle exec jekyll build --config ${ROOT_FOLDER}/_config.yml --source ${BUILD_FOLDER}/markdown_src --destination ${BUILD_FOLDER}/jekyll




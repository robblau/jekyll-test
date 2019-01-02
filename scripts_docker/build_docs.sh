#!/bin/bash

# make sure we are inside docker world
if [[ ! -v ROOT_FOLDER ]]; then
    echo "ROOT_FOLDER must be specified"
    exit 1
fi

# exit on error
set -e

BUILD_FOLDER=${ROOT_FOLDER}/_build
WEBSITE_FOLDER=${BUILD_FOLDER}/jekyll

echo "------------------------------------------------------"
echo "doc build process starting"
echo "------------------------------------------------------"

echo "cleaning out build location"
rm -rf ${ROOT_FOLDER}/_build

echo "creating build location"
mkdir ${BUILD_FOLDER}
mkdir ${BUILD_FOLDER}/markdown_src

echo "copying markdown docs scaffold into build locatio"
cp -r ${ROOT_FOLDER}/docs/* ${BUILD_FOLDER}/markdown_src

echo "cloning core..."
git clone --depth 1 https://github.com/shotgunsoftware/tk-core.git ${BUILD_FOLDER}/git/tk-core
export PYTHONPATH=$PYTHONPATH:${BUILD_FOLDER}/git/tk-core/python

echo "converting sphinx -> markdown"
sphinx-build -b markdown -c ${ROOT_FOLDER}/sphinx -D project='foo' -D release='bar' -D version='0.0.0' ${BUILD_FOLDER}/git/tk-core/docs ${BUILD_FOLDER}/markdown_src/tk-core

echo "building jekyll site"
JEKYLL_ENV=production bundle exec jekyll build --config ${ROOT_FOLDER}/jekyll/_config.yml --source ${BUILD_FOLDER}/markdown_src --destination ${WEBSITE_FOLDER}


echo "------------------------------------------------------"
echo "All done. Build in ${WEBSITE_FOLDER}"
echo "------------------------------------------------------"


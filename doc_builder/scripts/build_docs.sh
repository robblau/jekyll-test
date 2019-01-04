#!/bin/bash

# exit on error
set -e

for i in "$@"
do
case $i in
    -u=*|--url=*)
    URL="${i#*=}"
    shift # past argument=value
    ;;
    -p=*|--url-path=*)
    URLPATH="${i#*=}"
    shift # past argument=value
    ;;
    -s=*|--source=*)
    SOURCE="${i#*=}"
    shift # past argument=value
    ;;
    -o=*|--output=*)
    OUTPUT="${i#*=}"
    shift # past argument=value
    ;;
    *)
          # unknown option
    ;;
esac
done

echo "---------------------------------------------------"
echo "DOC BUILD"
echo "Source = ${SOURCE}"
echo "Output = ${OUTPUT}"
echo "Url    = ${URL}${URLPATH}"
echo "---------------------------------------------------"

THIS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

TMP_BUILD_FOLDER=${THIS_DIR}/../_build/markdown_src
WEBSITE_FOLDER=${OUTPUT}

echo "cleaning out internal build location '${TMP_BUILD_FOLDER}'..."
rm -rf ${TMP_BUILD_FOLDER}

echo "cleaning out final build location '${WEBSITE_FOLDER}'..."
rm -rf ${WEBSITE_FOLDER}

echo "creating build location"
mkdir -p ${TMP_BUILD_FOLDER}

echo "copying markdown docs scaffold into build location"
cp -r ${SOURCE}/* ${TMP_BUILD_FOLDER}

echo "running sphinx builds..."
python {THIS_DIR}/build_sphinx.py ${TMP_BUILD_FOLDER}


echo "cloning core..."
TMP_SPHINX_FOLDER=${TMP_BUILD_FOLDER}_spx
rm -rf ${TMP_SPHINX_FOLDER}
mkdir -p ${TMP_SPHINX_FOLDER}

git clone --depth 1 https://github.com/shotgunsoftware/tk-core.git ${TMP_SPHINX_FOLDER}/git/tk-core
export PYTHONPATH=$PYTHONPATH:${TMP_SPHINX_FOLDER}/git/tk-core/python

echo "converting sphinx -> markdown"
sphinx-build -b markdown -c ${THIS_DIR}/../sphinx -D project='foo' -D release='bar' -D version='0.0.0' ${TMP_SPHINX_FOLDER}/git/tk-core/docs ${TMP_BUILD_FOLDER}/tk-core

git clone --depth 1 https://github.com/shotgunsoftware/tk-framework-shotgunutils.git ${TMP_SPHINX_FOLDER}/git/tk-framework-shotgunutils
export PYTHONPATH=$PYTHONPATH:${TMP_SPHINX_FOLDER}/git/tk-framework-shotgunutils/python

echo "converting sphinx -> markdown"
sphinx-build -b markdown -c ${THIS_DIR}/../sphinx -D project='foo' -D release='bar' -D version='0.0.0' ${TMP_SPHINX_FOLDER}/git/tk-framework-shotgunutils/docs ${TMP_BUILD_FOLDER}/tk-framework-shotgunutils



echo "building jekyll site"
BUNDLE_GEMFILE=${THIS_DIR}/../Gemfile JEKYLL_ENV=production \
bundle exec jekyll build \
--baseurl ${URLPATH} --config ${THIS_DIR}/../jekyll/_config.yml \
--source ${TMP_BUILD_FOLDER} --destination ${OUTPUT}


echo "------------------------------------------------------"
echo "Build completed."
echo "------------------------------------------------------"


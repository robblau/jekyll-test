#!/bin/bash


export ROOT_FOLDER=${TRAVIS_BUILD_DIR}


THIS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

${THIS_DIR}/../scripts_docker/build_docs.sh


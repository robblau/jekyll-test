#!/bin/bash

THIS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

docker build ${THIS_DIR}/.. -t tk-docs && \
docker run --env ROOT_FOLDER=/app --mount type=bind,source="${THIS_DIR}/..",target=/app tk-docs


#!/bin/bash

THIS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

docker build ${THIS_DIR}/../doc_builder -t tk-docs && \
docker run -it --mount type=bind,source="${THIS_DIR}/..",target=/app tk-docs bash

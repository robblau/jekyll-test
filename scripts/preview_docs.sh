#!/bin/bash

THIS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

$THIS_DIR/build_docs.sh && open $THIS_DIR/../_build/jekyll/index.html
#!/usr/bin/env bash
set -e # halt script on error


if [ "$TRAVIS_PULL_REQUEST" != "false" ] ; then

    # upload to S3
    python ./ci_s3_upload.py

    # add comment to PR
    curl -H "Authorization: token ${GITHUB_TOKEN}" -X POST \
    -d "{\"body\": \"Doc Preview here: https://foo.bar/sgpipelinetest/${TRAVIS_BUILD_NUMBER}/index.html\"}" \
    "https://api.github.com/repos/${TRAVIS_REPO_SLUG}/issues/${TRAVIS_PULL_REQUEST}/comments"


fi


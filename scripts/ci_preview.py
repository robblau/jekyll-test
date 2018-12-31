print "hello python world"

import boto3
import os
import sys

print boto3

print "PULL REQUEST STATUS: %s" % os.environ.get("TRAVIS_PULL_REQUEST")

import sphinx
print sphinx

if os.environ.get("TRAVIS_PULL_REQUEST") == "false":



    cmd =  "curl -H 'Authorization: token ${GITHUB_TOKEN}' -X POST "
    cmd += "-d '{\"body\": \"Doc Preview here: https://foo.bar/sgpipelinetest/${TRAVIS_BUILD_NUMBER}/index.html\"}' "
    cmd += "'https://api.github.com/repos/${TRAVIS_REPO_SLUG}/issues/${TRAVIS_PULL_REQUEST}/comments'"
    print 'executing command %s' % cmd
    os.system(cmd)

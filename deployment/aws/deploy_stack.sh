#!/bin/bash
#
# Requires lambda_deployfile.zip is already pushed to the S3 deployment bucket
# Will fail if stack already exists
#

# Get S3BUCKET from environment or use default:
S3BUCKET=${S3BUCKET:-chipmonkey.json}

set -e
aws cloudformation validate-template --template-body file://cloudformation.yml

set +e
if aws cloudformation deploy --template-file ./cloudformation.yml --stack-name monkeyStack --capabilities CAPABILITY_IAM \
    --parameter-overrides S3BucketName=$(S3BUCKET)
then
aws cloudformation describe-stacks --stack-name monkeyStack
else
aws cloudformation describe-stack-events --stack-name monkeyStack
fi

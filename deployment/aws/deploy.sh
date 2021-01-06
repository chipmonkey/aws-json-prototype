#!/bin/bash
#
# Requires lambda_deployfile.zip is already pushed to the S3 deployment bucket
#
set -e
aws cloudformation validate-template --template-body file://cloudformation.yml
aws cloudformation delete-stack --stack-name monkeyStack
aws cloudformation wait stack-delete-complete --stack-name monkeyStack

set +e
if aws cloudformation deploy --template-file ./cloudformation.yml --stack-name monkeyStack --capabilities CAPABILITY_IAM \
    --parameter-overrides S3BucketName=chipmonkey.json
then
aws cloudformation describe-stacks --stack-name monkeyStack
else
aws cloudformation describe-stack-events --stack-name monkeyStack
fi

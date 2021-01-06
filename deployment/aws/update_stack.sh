#!/bin/bash
#
# Updates existing aws stack
#

set -e
aws s3 cp ./cloudformation.yml s3://chipmonkey.json/
# Parameterize this:
# aws lambda update-function-code --function-name monkeyStack-JSONLambda-AQHGX1GQFX8O --s3-bucket chipmonkey.json --s3-key lambda_deployfile.zip
aws cloudformation validate-template --template-body file://cloudformation.yml
aws cloudformation update-stack --template-url https://s3.amazonaws.com/chipmonkey.json/cloudformation.yml \
  --stack-name monkeyStack \
  --capabilities CAPABILITY_IAM \
  --parameters ParameterKey=S3BucketName,ParameterValue=chipmonkey.json


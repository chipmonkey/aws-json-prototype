#!/bin/bash
#
# Updates existing aws stack
#

# Get S3BUCKET name from environment variable or use default
S3BUCKET=${S3BUCKET:-chipmonkey.json}

set -e
aws s3 cp ./cloudformation.yml s3://$(S3BUCKET)/
# Parameterize this:
# aws lambda update-function-code --function-name monkeyStack-JSONLambda-JR87DLJY63E6  --s3-bucket $(S3BUCKET) --s3-key lambda_deployfile.zip
aws cloudformation validate-template --template-body file://cloudformation.yml
aws cloudformation update-stack --template-url https://s3.amazonaws.com/chipmonkey.json/cloudformation.yml \
  --stack-name monkeyStack \
  --capabilities CAPABILITY_IAM \
  --parameters ParameterKey=S3BucketName,ParameterValue=$(S3BUCKET)


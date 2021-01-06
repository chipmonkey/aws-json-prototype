#!/bin/bash
#
# Updates existing aws stack
#

echo "Using S3BUCKET: $S3BUCKET"

set -e
aws s3 cp ./cloudformation.yml s3://$S3BUCKET/
# Parameterize this:
# aws lambda update-function-code --function-name monkeyStack-JSONLambda-AQHGX1GQFX8O --s3-bucket $S3BUCKET --s3-key lambda_deployfile.zip
aws cloudformation validate-template --template-body file://cloudformation.yml
aws cloudformation update-stack --template-url https://s3.amazonaws.com/$S3BUCKET/cloudformation.yml \
  --stack-name monkeyStack \
  --capabilities CAPABILITY_IAM \
  --parameters ParameterKey=S3BucketName,ParameterValue=$S3BUCKET


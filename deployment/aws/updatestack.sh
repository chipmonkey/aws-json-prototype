set -e
aws s3 cp ./cloudformation.yml s3://chipmonkey.json/
aws cloudformation validate-template --template-body file://cloudformation.yml
aws cloudformation update-stack --template-url https://s3.amazonaws.com/chipmonkey.json/cloudformation.yml \
  --stack-name monkeyStack \
  --capabilities CAPABILITY_IAM \
  --parameters ParameterKey=S3BucketName,ParameterValue=chipmonkey.json


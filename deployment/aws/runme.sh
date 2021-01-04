set -e
aws cloudformation validate-template --template-body file://cloudformation.yml
aws s3 cp ../../parser/build/lambda_deployfile.zip s3://chipmonkey.json/
aws cloudformation delete-stack --stack-name monkeyStack
aws cloudformation wait stack-delete-complete --stack-name monkeyStack
aws cloudformation deploy --template-file ./cloudformation.yml --stack-name monkeyStack --capabilities CAPABILITY_IAM \
    --parameter-overrides S3BucketName=chipmonkey.json

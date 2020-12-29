aws cloudformation delete-stack --stack-name monkeyStack
aws cloudformation wait stack-delete-complete --stack-name monkeyStack
aws cloudformation deploy --template-file ./cloudformation.yml --stack-name monkeyStack --capabilities CAPABILITY_IAM # --on-failure DO_NOTHING

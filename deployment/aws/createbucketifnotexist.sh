if [ -z ${S3_BUCKET+x} ]
then
    if [[ $# -eq 0 ]]
    then
        echo "S3_BUCKET must be an environment variable or a parameter"
        exit 1
    fi
    S3_BUCKET=$1
fi

if aws s3api head-bucket --bucket "$S3_BUCKET" 2>/dev/null
then
    echo "s3://${S3_BUCKET} exists"
else
    echo "s3://${S3_BUCKET} does not exist... creating now..."
    aws s3 mb s3://${S3_BUCKET} --region us-east-1
    echo "done"
fi

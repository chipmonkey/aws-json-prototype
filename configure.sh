echo "Hello World"

if [ -f "myconfig" ];
then
  while true
  do
    read -p "myconfig exists... reconfigure? (y/n)" yn
    case $yn in
      [Yy]* ) break;;
      [Nn]* ) exit;;
      * ) echo "Please answer y or n (yes or no).";;
    esac
  done
fi

echo "Checking AWS Credentials"
until aws sts get-caller-identity
do
    echo "Credentials do not exist - calling aws configure"
    aws configure
done

echo "AWS CLI configured.  Run aws configure manually to change values."

echo "-------------------"
echo "Configuring AWS S3 Options"

thing=true
while $thing
do
    read -p "Enter a valid S3 Bucket Name for JSON and Code storage [chipmonkey.json]: " S3BUCKET
    S3BUCKET=${S3BUCKET:-chipmonkey.json}
    echo "name is: $S3BUCKET"
    # if [[ $S3BUCKET=~ (?=^.{3,63}$)(?!^(\d+\.)+\d+$)(^(([a-z0-9]|[a-z0-9][a-z0-9\-]*[a-z0-9])\.)*([a-z0-9]|[a-z0-9][a-z0-9\-]*[a-z0-9])$) ]]
    # see https://stackoverflow.com/questions/50480924/regex-for-s3-bucket-name
    if [[ $S3BUCKET =~ ^([0-9a-z.-]){3,63}$ ]]
    then
        echo "Works for me"
        thing=false
    else
        echo "Invalid S3 Bucket Name."
        echo "Bucket name must be between 3 and 63 characters long"
        echo "and must contain only lowercase letters, numbers, and periods (.)"
        echo "There are more rules but we don't check for them all here, so make good choices"
    fi
done

echo "S3BUCKET=$S3BUCKET" > myconfig
aws s3 mb s3://$S3BUCKET

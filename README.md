# PingSafe Webhook Lambda

## init.py
Creates AWS resources and deploys src/deployment-package.zip on lambda
AWS resourcess
- SQS Queue
- S3 Bucket
- IAM Role and Policies required for lambda
- Lifecycle rules for S3 (1-day expiration of objects)
- Lambda function 

### Requirements
- aws cli
- python3

## Steps to start
1. Clone this repository
```shell
git clone https://github.com/PingSafe/webhook-s3-sqs-workflow.git
```
2. Move to `webhook-s3-sqs-workflow` directory
```shell
cd webhook-s3-sqs-workflow
```
3. Execute below commands to install dependency and create AWS resources
```shell
pip3 install -r requirements.txt
python3 init.py --aws-cli-profile <aws cli profile> --aws-region <aws region> --queue-name <sqs queue name> --lambda-function-name <lambda name>
```

> NOTE: If running on a aws cloudshell or non profile based authenticatoion credentials, pass `<aws cli profile>` as `none`

> Copy the SQS url, Lambda url and PingSafe key provided in the output

In case `src/lambda_function.py` is changed, please add it to `deployment-package.zip` using

```shell
zip src/deployment-package.zip src/lambda_function.py
```

## Qradar setup steps:
    
1. Download the PingSafe DSM for QRadar from [here.](https://drive.google.com/file/d/1pXmw4nBQhtEd9gk-XWl2IN8EXLmX-Wq8/view?usp=share_link) 
2. Open **Admin dashboard**->**Extension Management**. From there add the "PingSafe" extension (check install immediately).
3. Open **Log Source Management App**. Create a new single Log Source
    1. Select “PingSafe” as Log source type. Click on next.
    2. Select “Amazon AWS S3 Rest API“ as Protocol. Click on next.
    3. Configure Log Source parameters:
        *  Name = _Any suitable name for your log source_
        *  Extension = _select PingSafeCustom_ext extension_
        *  Coalescing Events = _set this to off_
        >  Leave rest of the details on this page as it is.
    4. Configure Protocol parameters:
          1.  Log source identifier = _enter name of your SQS queue_
          2.  Authentication Method = _select “Access key ID / Secret Key”_
          3.  Enter AWS Access key and Secret for user which has permission to read and delete action to SQS queue and read permission from S3.
          4.  Collection method = _select “SQS Event notification”_
          5.  SQS Queue URL = _enter the SQS url you copied earlier_
          6.  Region name = _Region of your SQS_
          7.  Event Format = _select LINEBYLINE_
          >  Leave the rest as it is.
4. Go to Admin dashboard and _Deploy Changes_ for Log Source to be activated.


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
```shell
pip3 install -r requirements.txt
python3 init.py --aws-cli-profile <aws cli profile> --aws-region <aws region> --queue-name <sqs queue name> --lambda-function-name <lambda name>
```

In case `src/lambda_function.py` is changed, please add it to `deployment-package.zip` using
> Copy the SQS url, Lambda url and PingSafe key provided in the output
```shell
zip src/deployment-package.zip src/lambda_function.py
```

## Qradar setup steps:
    
1.  Open **Admin dashboard**->**Extension Management**. From there add the "PingSafe" extension (check install immediately).
2.  Open **Log Source Management App**. Create a new single Log Source
    1.  Select “PingSafe” as Log source type. Next.
    2.  Select “Amazon AWS S3 Rest API“ as Protocol. Next.
    3.  Configure Log Source parameters:
        *  Name = _Any suitable name for your log source_
        *  Extension = _select PingSafe extension_
        *  Coalescing Events = _set this to off_
        >  Leave rest of the details on this page as it is.
    4.  Configure Protocol parameters:

          1.  Log source identifier = _enter name of your SQS_
          2.  Authentication Method = _select “Access key ID / Secret Key”_
          3.  Enter AWS Access key and Secret
          4.  Collection method = _select “SQS Event notification”_
          5.  SQS Queue URL = _enter the SQS url you copied earlier_
          6.  Region name = _Region of your SQS_
          7.  Event Format = _select LINEBYLINE_
          >  Leave the rest as it is.

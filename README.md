# PingSafe Webhook Lambda

### init.py
Creates AWS resources and deploys src/deployment-package.zip on lambda
AWS resourcess
- SQS Queue
- IAM Role and Policies required for lambda
- Lambda function 

Requirements
- aws cli
- python3

Steps to start
```shell
pip3 install -r requirements.txt
python3 init.py --aws-cli-profile <aws cli profile> --aws-region <aws region> --queue-name <sqs queue name> --lambda-function-name <lambda name>
```

In case src/lambda_function.py is changed, please add it to deployment-package.zip using
```shell
zip src/deployment-package.zip src/lambda_function.py
```


Qradar setup steps:
    
  1.  Open **Admin dashboard**->**Extension Management**. From there add the PingSafe extension (check install immediately).

  2.  Open **Log Source Management App**. Create a new single Log Source.

      1.  Select “PingSafe” as Log source type. Next.

      2.  Select “Amazon AWS S3 Rest API“ as Protocol. Next.

      3.  Configure Log Source parameters:

          1.  Name = Any suitable name for your log source

          2.  Extension = select PingSafe extension

          3.  Coalescing Events = set this to off.

          4.  Leave rest of the details on this page as it is.

      4.  Configure Protocol parameters:

          1.  Log source identifier = enter name of your SQS.

          2.  Authentication Method = select “Access key ID / Secret Key”

          3.  Enter AWS Access key and Secret

          4.  Collection method = select “SQS Event notification”

          5.  SQS Queue URL = enter the SQS url you copied earlier.

          6.  Region name = Region of your SQS.

          7.  Event Format = select LINEBYLINE

          8.  Leave the rest as it is.

      5.  Finish.

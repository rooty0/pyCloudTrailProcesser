# pyCloudTrailProcesser
Python AWS Lambda function to parse CloudTrail Logs for AWS Console Changes and Publish to SNS

## Configuration Service Lambda

### To build the package use Makefile
Make sure you have docker installed and configured
```shell script
make
```
The command above produces `config-service-lambda-deployment-package.zip` target that you can deploy directly to lambda using command below:
```shell script
# Create an EMPTY lambda function with name "cloudtrail-watcher" (changeable in Makefile - make sure it's lowercase)
# Then run the following command to deploy actual code
make deploy
```
See `Makefile` for more details. To clean everything after the build use following command
```shell script
make clean
```
Another example how to upload new version of function after some changes
```bash
make REGION=us-west-1 clean build deploy
```

## Environment variables
The following environment variables required by AWS Lambda
* `SNS_ARN`: the ARN of the SNS topic that you want to publish to 
* `IGNORE_EVENT_SOURCES`: optional variable to ignore event sources
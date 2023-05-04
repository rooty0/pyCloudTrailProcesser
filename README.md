# pyCloudTrailProcesser
Python AWS Lambda function to parse CloudTrail Logs for AWS Console manual changes and notifies you about the changes

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

###
To test function do something like
```bash
aws logs tail "/aws/lambda/cloudtrail-watcher" --region us-west-1 --follow
aws ec2 create-tags --resources i-060d00000000fd95b --tags "Key=TrStanFindMe,Value=$(date +%s)" --region us-east-1
```

## Environment variables
The following environment variables acceptable by AWS Lambda
* `NOTIFICATION_PLATFORM`: send notifications using `SNS` and/or `SLACK` (default: `SNS, SLACK`)
* `SNS_ARN`: the ARN of the SNS topic that you want to publish to 
* `SLACK_BOT_TOKEN`: OAuth token, you need to create an app to [generate](https://api.slack.com/enterprise/apps) one
* `SLACK_CHANNEL_ID`: id of a Slack channel, required if you use `SLACK` notification (example: `C0112ML201K`)
* `IGNORE_EVENT_SOURCES`: optional variable to ignore event sources

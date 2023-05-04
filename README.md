# pyCloudTrailProcesser
Python AWS Lambda function parses CloudTrail Logs to find AWS Console manual changes and notifies you about the changes

This project is an improved fork of the original [pyCloudTrailProcesser](https://github.com/matthew-harper/pyCloudTrailProcesser) from Matthew Harper. The original version is broken, too noisy, and pretty limited

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

### Other configuration
Don't forget to change the lambda function timeout (max runtime). A default value of 3 seconds sometimes is not enough to parse logs and send results back to you
```bash
aws lambda update-function-configuration --function-name cloudtrail-watcher --timeout 10
```

###
To see logs and test function do something like
```bash
aws logs tail "/aws/lambda/cloudtrail-watcher" --region us-west-1 --follow  # where "cloudtrail-watcher" is your function name
aws ec2 create-tags --resources i-060d00000000fd95b --tags "Key=TrStanFindMe,Value=$(date +%s)" --region us-east-1
```

## Environment variables
The following environment variables acceptable by AWS Lambda
* `NOTIFICATION_PLATFORM`: send notifications using `SNS` and/or `SLACK` (default: `SNS, SLACK`)
* `SNS_ARN`: the ARN of the SNS topic that you want to publish to 
* `SLACK_BOT_TOKEN`: OAuth token, you need to create an app to [generate](https://api.slack.com/enterprise/apps) one
* `SLACK_CHANNEL_ID`: id of a Slack channel, required if you use `SLACK` notification (example: `C0112ML201K`)
* `IGNORE_EVENT_SOURCES`: optional variable to ignore event sources (example: `athena.amazonaws.com, somestuff.amazon.com`)
* `NOTIFY_ALL_ACCESS_ISSUES`: option enables a special mode allowing you to receive ALL access issue (Access Denied) notifications regardless of whether it was a manual change. Please note you also get all read-only access denied events (default: `no`)
* `NOTIFY_ALL_ACCESS_ISSUES_EXCLUDE_EVENT`: list of event names to exclude from all access denied notify (example: `ListNotificationHubs, SomeStuffBoom`)

An example how to setup environment variables with `aws cli`:
```bash
aws lambda update-function-configuration --function-name cloudtrail-watcher \
    --environment "Variables={IGNORE_EVENT_SOURCES=athena.amazonaws.com,NOTIFICATION_PLATFORM=SLACK,NOTIFY_ALL_ACCESS_ISSUES=yes,NOTIFY_ALL_ACCESS_ISSUES_EXCLUDE_EVENT=ListNotificationHubs,SLACK_BOT_TOKEN=xoxb-93,SLACK_CHANNEL_ID=aaaa}"
```

## Contribute
Feel free to create a PR 

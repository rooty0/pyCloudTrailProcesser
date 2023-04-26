import json
import urllib.parse
import boto3
import io
import gzip
import re
import os
import slack_sdk
import slack_template

from slack_sdk.errors import SlackApiError
from time import sleep

__version__ = 2.0

s3 = boto3.client('s3')
sns = boto3.client('sns')
sns_arn = os.environ.get('SNS_ARN', '')
SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN', '')
SLACK_CHANNEL_ID = os.environ.get('SLACK_CHANNEL_ID', '')

USER_AGENTS = {i.strip() for i in os.environ.get(
    'USER_AGENTS',
    'console.amazonaws.com, Coral/Jakarta, Coral/Netty4'
).split(",")}
USER_AGENT_DETECT_METHOD = os.environ.get('USER_AGENT_DETECT_METHOD', 'INCLUSIVE').lower()  # inclusive / exclusive

IGNORED_EVENTS = {
    "DownloadDBLogFilePortion", "TestScheduleExpression", "TestEventPattern", "LookupEvents",
    "listDnssec", "Decrypt", "REST.GET.OBJECT_LOCK_CONFIGURATION", "ConsoleLogin",
    "Authenticate", "Federate", "UserAuthentication", "CreateToken",  # SSO
    "SendSSHPublicKey", "SendSerialConsoleSSHPublicKey",  # SSH to EC2 from AWS WebUI
}
IGNORED_EVENT_SRCS = {i.strip() for i in os.environ.get('IGNORE_EVENT_SOURCES', '').split(",")}
NOTIFICATION_PLATFORM = {i.strip() for i in os.environ.get('NOTIFICATION_PLATFORM', 'SNS, SLACK').split(",")}
NOTIFY_ALL_ACCESS_ISSUES = True if os.environ.get('NOTIFY_ALL_ACCESS_ISSUES', 'yes') == 'yes' else False


def post_notification(records) -> None:

    if 'SNS' in NOTIFICATION_PLATFORM:
        for item in records:
            post_to_sns(
                get_user_email(item['userIdentity']['principalId']),
                item['eventName'],
                item['eventID']
            )
        # Posting detailed report
        post_to_sns_details(records)

    if 'SLACK' in NOTIFICATION_PLATFORM:
        slack = slack_sdk.WebClient(token=SLACK_BOT_TOKEN)
        for item in records:
            post_to_slack(slack, item)

    if 'STDOUT' in NOTIFICATION_PLATFORM:
        # reserved future use (useful for debug)
        pass


def post_to_slack(client, record) -> None:
    user_email = get_user_email(record['userIdentity']['principalId'])
    event_name = record.get('eventName')
    event_id = record.get('eventID')
    message = slack_template.SlackTemplate(
        email=user_email,
        user_identity=record.get('userIdentity', {}).get('principalId', 'UNKNOWN'),
        event_name=event_name,
        event_source=record.get('eventSource'),
        event_id=event_id,
        event_time=record.get('eventTime'),
        error=record.get('errorMessage') if 'errorMessage' in record else record.get('errorCode', '')
    )
    try:
        response = client.chat_postMessage(
            channel=SLACK_CHANNEL_ID,
            attachments=[message.render_attachment()],
            text=f"Manual AWS Changes Detected: "
                 f"*<mailto:{user_email}|{user_email}>* --> *{event_name}* (Event ID: _{event_id}_)",
        )
        sleep(0.5)  # looks like Slack doesn't like it when we send it right away?
        client.files_upload_v2(
            channel=SLACK_CHANNEL_ID,
            thread_ts=response.data['ts'],
            title='Review Full LOG',
            filename=f"full_log_{record.get('eventID')}.json",
            content=json.dumps(
                record, indent=4, sort_keys=True, ensure_ascii=False, separators=(',', ': ')
            )
        )

    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        print(e.response["error"])
        raise e


def post_to_sns(user, event_name, event_id) -> None:
    message = f"Manual AWS Changed Detected:  {user} --> {event_name} (Event ID: {event_id})"
    sns_publish(message)


def post_to_sns_details(message) -> None:
    message = {"Manual AWS Change Detected": message}
    sns_publish(message)


def sns_publish(message) -> None:
    if sns_arn:
        sns.publish(
            TargetArn=sns_arn,
            Message=json.dumps(
                {
                    'default': json.dumps(
                        message, indent=4, sort_keys=True, ensure_ascii=False, separators=(',', ': ')
                    )
                }
            ),
            MessageStructure='json'
        )


def check_regex(expr, txt) -> bool:
    match = re.search(expr, txt)
    return match is not None


def check_user_agent(txt) -> bool:

    if 'inclusive' in USER_AGENT_DETECT_METHOD:
        return match_user_agent(txt)
    else:
        raise Exception("Not supported")


def match_user_agent(txt) -> bool:
    """
    TODO:
      !!! Consider to whitelist terraform and blacklist everything else !!!

    :param str txt: user agent to parse
    :return: true if client considered as manual change
    """
    if txt in USER_AGENTS:
        return True

    expressions = (
        "signin.amazonaws.com(.*)",
        "^S3Console",
        "^\[S3Console",
        "^Mozilla/",
        "^console(.*)amazonaws.com(.*)",
        "^aws-internal(.*)AWSLambdaConsole(.*)",
        "^aws-cli/",
    )

    for expresion in expressions:
        if check_regex(expresion, txt):
            return True

    return False


def match_readonly_event_name(txt) -> bool:
    # starts with
    expressions = (
        "^Get",
        "^Describe",
        "^List",
        "^Head",
    )
    for expression in expressions:
        if check_regex(expression, txt):
            return True

    return False


def match_ignored_events(event_name) -> bool:
    return event_name in IGNORED_EVENTS


def match_ignored_event_sources(event_source) -> bool:
    return event_source in IGNORED_EVENT_SRCS


def filter_user_events(event) -> bool:
    is_match = check_user_agent(event.get('userAgent', ''))
    is_read_only = event['readOnly']
    is_ignored_event = match_ignored_events(event['eventName'])
    if_ignored_event_source = match_ignored_event_sources(event['eventSource'])
    is_in_event = 'invokedBy' in event['userIdentity'] and event['userIdentity']['invokedBy'] == 'AWS Internal'

    # from pprint import pprint
    # if not is_read_only:
    #     print("Event ID: {} / is_match: {} / is_ignored_event: {} / is_in_event: {}"
    #           .format(event.get('requestID', 'UNKNOWN'), is_match, is_ignored_event, is_in_event))

    if NOTIFY_ALL_ACCESS_ISSUES and event.get('errorCode', '') == 'AccessDenied':
        return True

    status = is_match and not is_read_only and not is_ignored_event and not if_ignored_event_source and not is_in_event

    return status


def get_user_email(principal_id) -> str:
    words = principal_id.split(':')
    if len(words) > 1:
        return words[1]
    return principal_id


def lambda_handler(event, context) -> None:
    """
    This functions processes CloudTrail logs from S3, filters events from the AWS Console, and publishes to SNS
    :param event: List of S3 Events
    :param context: AWS Lambda Context Object
    :return: None
    """
    for record in event['Records']:
        # Get the object from the event and show its content type
        bucket = record['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(record['s3']['object']['key'], encoding='utf-8')
        try:
            response = s3.get_object(Bucket=bucket, Key=key)
            content = response['Body'].read()

            with gzip.GzipFile(fileobj=io.BytesIO(content), mode='rb') as fh:
                event_json = json.load(fh)
                output_dict = [record for record in event_json['Records'] if filter_user_events(record)]
                if len(output_dict) > 0:
                    print(
                        f"Found {len(output_dict)} manual changes. "
                        f"Event ID: {[i.get('eventID', 'UNKNOWN') for i in output_dict]} "
                        f"at S3://{bucket}/{key}"
                    )

                    post_notification(output_dict)

            return response['ContentType']
        except Exception as e:
            print(e)
            print(f"Error getting object {key} from bucket {bucket}")
            raise e


def unit_test() -> None:
    import record_example
    event_json = record_example.structure
    output_dict = [record for record in event_json['Records'] if filter_user_events(record)]

    if len(output_dict) > 0:
        print(
            f"Found {len(output_dict)} manual changes by {'(INCLUDING ACCESS DENIED)' if NOTIFY_ALL_ACCESS_ISSUES else ''}"
        )

        for item in output_dict:
            user_email = get_user_email(item['userIdentity']['principalId'])
            print(f"  - {user_email}: {item['eventName']}")

        post_notification(output_dict)


if __name__ == '__main__':
    unit_test()

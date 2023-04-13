import json
import urllib.parse
import boto3
import io
import gzip
import re
import os

s3 = boto3.client('s3')
sns = boto3.client('sns')
sns_arn = os.environ.get('SNS_ARN', '')

USER_AGENTS = {"console.amazonaws.com", "Coral/Jakarta", "Coral/Netty4"}
IGNORED_EVENTS = {
    "DownloadDBLogFilePortion", "TestScheduleExpression", "TestEventPattern", "LookupEvents",
    "listDnssec", "Decrypt", "REST.GET.OBJECT_LOCK_CONFIGURATION", "ConsoleLogin",
    "Authenticate", "Federate", "UserAuthentication"  # SSO
}
IGNORED_EVENT_SRCS = {i.strip() for i in os.environ.get('IGNORE_EVENT_SOURCES', '').split(",")}


#
# Slack support https://github.com/matthew-harper/pyCloudTrailProcesser/compare/master...slitsevych:lambda-cloudtrail-parser:master?diff=split
#
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
                        message, indent=4, sort_keys=False, ensure_ascii=False, separators=(',', ': ')
                    )
                }
            ),
            MessageStructure='json'
        )


def check_regex(expr, txt) -> bool:
    match = re.search(expr, txt)
    return match is not None


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
    is_match = match_user_agent(event.get('userAgent', ''))
    is_read_only = event['readOnly']
    is_ignored_event = match_ignored_events(event['eventName'])
    if_ignored_event_source = match_ignored_event_sources(event['eventSource'])
    is_in_event = 'invokedBy' in event['userIdentity'] and event['userIdentity']['invokedBy'] == 'AWS Internal'

    # from pprint import pprint
    # if not is_read_only:
    #     print("Event ID: {} / is_match: {} / is_ignored_event: {} / is_in_event: {}"
    #           .format(event.get('requestID', 'UNKNOWN'), is_match, is_ignored_event, is_in_event))

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
                        f"Request ID(s): {[i.get('requestID', 'UNKNOWN') for i in output_dict]}"
                    )
                    for item in output_dict:
                        post_to_sns(
                            get_user_email(item['userIdentity']['principalId']),
                            item['eventName'],
                            item['eventID']
                        )
                    # Posting detailed report
                    post_to_sns_details(output_dict)

            return response['ContentType']
        except Exception as e:
            print(e)
            print(f"Error getting object {key} from bucket {bucket}")
            raise e


def unit_test() -> None:
    with open('sample.txt') as json_file:
        event_json = json.load(json_file)
        output_dict = [record for record in event_json['Records'] if filter_user_events(record)]
        for item in output_dict:
            user_email = get_user_email(item['userIdentity']['principalId'])
            print('Manual changes:')
            print(f"{user_email} -- {item['eventName']}")
            post_to_sns(get_user_email(item['userIdentity']['principalId']), item['eventName'])
            post_to_sns_details(item)


if __name__ == '__main__':
    unit_test()

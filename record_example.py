data_container = \
    [
        # Sample 1
        {'awsRegion': 'us-east-1',
         'eventCategory': 'Management',
         'eventID': 'dc0c14ae-72ae-4025-aaf7-b9707500adff',
         'eventName': 'CreateTags',
         'eventSource': 'ec2.amazonaws.com',
         'eventTime': '2023-04-13T19:56:38Z',
         'eventType': 'AwsApiCall',
         'eventVersion': '1.08',
         'managementEvent': True,
         'readOnly': False,
         'recipientAccountId': '062000000000',
         'requestID': 'f2fb72f3-18bc-4233-937c-8341d7bd2cde',
         'requestParameters': {'resourcesSet': {'items': [{'resourceId': 'i-060d00000000fd95b'}]},
                               'tagSet': {'items': [{'key': 'TestTag',
                                                     'value': 'my_tag_value'}]}},
         'responseElements': {'_return': True,
                              'requestId': 'f2fb72f3-18bc-4233-937c-8341d7bd2cde'},
         'sourceIPAddress': '50.200.00.200',
         'tlsDetails': {'cipherSuite': 'ECDHE-RSA-AES128-GCM-SHA256',
                        'clientProvidedHostHeader': 'ec2.us-east-1.amazonaws.com',
                        'tlsVersion': 'TLSv1.2'},
         'userAgent': 'aws-cli/2.11.8 Python/3.11.2 Darwin/21.6.0 source/arm64 '
                      'prompt/off command/ec2.create-tags',
         'userIdentity': {'accessKeyId': 'ASIAQ52IPRMBGR1W77WH',
                          'accountId': '062000000000',
                          'arn': 'arn:aws:sts::062000000000:assumed-role/AWSReservedSSO_Admins_260008d6b2140109/example@domain.com',
                          'principalId': 'AROAQ24IPRMBUNTPNGG1D:example@domain.com',
                          'sessionContext': {'attributes': {'creationDate': '2023-04-13T19:38:02Z',
                                                            'mfaAuthenticated': 'false'},
                                             'sessionIssuer': {'accountId': '062227712770',
                                                               'arn': 'arn:aws:iam::062000000000:role/aws-reserved/sso.amazonaws.com/us-west-2/AWSReservedSSO_Admins_260008d6b2140109',
                                                               'principalId': 'AROAQ24IPRMBUNTPNGG1D',
                                                               'type': 'Role',
                                                               'userName': 'AWSReservedSSO_Admins_260008d6b2140109'},
                                             'webIdFederationData': {}},
                          'type': 'AssumedRole'}},
        # Sample 2
        {}
    ]

structure = {
    'Records': data_container
}

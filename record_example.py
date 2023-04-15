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
                                             'sessionIssuer': {'accountId': '062000000000',
                                                               'arn': 'arn:aws:iam::062000000000:role/aws-reserved/sso.amazonaws.com/us-west-2/AWSReservedSSO_Admins_260008d6b2140109',
                                                               'principalId': 'AROAQ24IPRMBUNTPNGG1D',
                                                               'type': 'Role',
                                                               'userName': 'AWSReservedSSO_Admins_260008d6b2140109'},
                                             'webIdFederationData': {}},
                          'type': 'AssumedRole'}},
        # Sample 2
        {
            'eventVersion': '1.08',
            'userIdentity': {
                'type': 'AssumedRole',
                'principalId': 'AROAQ23IPRMBDBOXLCVCW:user@example.com',
                'arn': 'arn:aws:sts::062000000000:assumed-role/AWSReservedSSO_AAA_b024b126c27b1008/user@example.com',
                'accountId': '062000000000',
                'accessKeyId': 'ASIAQ12IPRMBNZ00ME4W',
                'sessionContext': {
                    'sessionIssuer': {
                        'type': 'Role',
                        'principalId': 'AROAQ23IPRMBDBOXLCVCW',
                        'arn': 'arn:aws:iam::062000000000:role/aws-reserved/sso.amazonaws.com/us-west-2/AWSReservedSSO_AAA_b024b126c27b1008',
                        'accountId': '062000000000',
                        'userName': 'AWSReservedSSO_AAA_b024b126c27b1008'
                    },
                    'webIdFederationData': {},
                    'attributes': {
                        'creationDate': '2023-04-13T21:11:11Z',
                        'mfaAuthenticated': 'false'
                    }
                }
            },
            'eventTime': '2023-04-13T21:14:34Z',
            'eventSource': 's3.amazonaws.com',
            'eventName': 'CreateBucket',
            'awsRegion': 'us-west-2',
            'sourceIPAddress': '24.8.100.100',
            'userAgent': '[S3Console/0.4, aws-internal/3 aws-sdk-java/1.11.1030 Linux/5.4.238-155.347.amzn2int.x86_64 OpenJDK_64-Bit_Server_VM/25.362-b10 java/1.8.0_362 vendor/Oracle_Corporation cfg/retry-mode/standard]',
            'errorCode': 'AccessDenied',
            'errorMessage': 'Access Denied',
            'requestParameters': {
                'CreateBucketConfiguration': {
                    'LocationConstraint': 'us-west-2',
                    'xmlns': 'http://s3.amazonaws.com/doc/2006-03-01/'
                },
                'bucketName': 'cc-aaa-model',
                'Host': 's3.us-west-2.amazonaws.com',
                'x-amz-object-ownership': 'BucketOwnerEnforced'
            },
            'responseElements': None,  # was Null here, I'm guessing it converts to 'None'
            'additionalEventData': {
                'SignatureVersion': 'SigV4',
                'CipherSuite': 'ECDHE-RSA-AES128-GCM-SHA256',
                'bytesTransferredIn': 153,
                'AuthenticationMethod': 'AuthHeader',
                'x-amz-id-2': 'aaaaa=',
                'bytesTransferredOut': 243
            },
            'requestID': 'MA5EFSC5JZG8FE51',
            'eventID': '54e06abd-59cd-4a1c-9b8e-410757e1e156',
            'readOnly': False,
            'eventType': 'AwsApiCall',
            'managementEvent': True,
            'recipientAccountId': '062000000000',
            'vpcEndpointId': 'vpce-a0d039c0',
            'eventCategory': 'Management',
            'tlsDetails': {
                'tlsVersion': 'TLSv1.2',
                'cipherSuite': 'ECDHE-RSA-AES128-GCM-SHA256',
                'clientProvidedHostHeader': 's3.us-west-2.amazonaws.com'
            }
        },
        # Sample 3
        {
            'eventVersion': '1.08',
            'userIdentity': {
                'type': 'Unknown',
                'principalId': '9267091f00-85ad01b2-b212-41c3-3fff-5801e02738b1',
                'accountId': '062000000000',
                'userName': 'John Doe'
            },
            'eventTime': '2023-04-14T17:55:10Z',
            'eventSource': 'sso.amazonaws.com',
            'eventName': 'CreateToken',
            'awsRegion': 'us-west-2',
            'sourceIPAddress': '174.99.100.100',
            'userAgent': 'aws-cli/2.9.23 Python/3.11.2 Darwin/22.4.0 source/x86_64 prompt/off command/sso.login',
            'requestParameters': {
                'clientId': 'jtRE3hrPl0MKPSjXs90fl3VzLXalc4QtPb',
                'clientSecret': 'HIDDEN_DUE_TO_SECURITY_REASONS',
                'grantType': 'urn:ietf:params:oauth:grant-type:device_code',
                'deviceCode': '1G00cDVBGPt00MPHx-dAPRKVJKhiTmR0RDGPqcuiGTSQTvvE0-0ZDolXapoQbt0xTeQ_eWu3cqYXJdISKPPEFA',
                'platformSessionExpiryRequired': False
            },
            'responseElements': {
                'accessToken': 'HIDDEN_DUE_TO_SECURITY_REASONS',
                'tokenType': 'Bearer',
                'expiresIn': 28796,
                'refreshToken': 'HIDDEN_DUE_TO_SECURITY_REASONS',
                'idToken': 'HIDDEN_DUE_TO_SECURITY_REASONS'
            },
            'requestID': 'fe1df0dc-b004-00ab-ba8e-1f0c0a6fb9d0',
            'eventID': '79a5c7b0-01e8-0da4-9aa2-687da8a000a6',
            'readOnly': False,
            'resources': [
                {
                    'accountId': '062000000000',
                    'type': 'IdentityStoreId',
                    'ARN': 'd-9267091f00'
                }
            ],
            'eventType': 'AwsApiCall',
            'managementEvent': True,
            'recipientAccountId': '062000000000',
            'eventCategory': 'Management',
            'tlsDetails': {
                'tlsVersion': 'TLSv1.2',
                'cipherSuite': 'ECDHE-RSA-AES128-GCM-SHA256',
                'clientProvidedHostHeader': 'oidc.us-west-2.amazonaws.com'
            }
        }
    ]

structure = {
    'Records': data_container
}

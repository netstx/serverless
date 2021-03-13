import boto3
import json
import os
from botocore.exceptions import ClientError
from botocore.vendored import requests

def send_email(sender, recipient, aws_region, subject, smsfrom, smsto, smsmessage, smstimestamp):
    # This address must be verified with Amazon SES.
    SENDER = sender

    # If your account is still in the sandbox, this address must be verified.
    RECIPIENT = recipient

    # The AWS Region you're using for Amazon SES.
    AWS_REGION = aws_region

    # The subject line for the email.
    SUBJECT = subject

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = "SMS received"

    # The HTML body of the email.
    BODY_HTML = """<html><head></head><body><table><tbody><tr><td>From:</td><td>""" + smsfrom + """</td></tr><tr><td>To:</td><td>""" + smsto + """</td></tr><tr><td>Body:</td><td>""" + smsmessage + """</td></tr><tr><td>Time:</td><td>""" + smstimestamp + """</td></tr></tbody></table></body></html>"""

    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses', region_name=AWS_REGION)

    # Try to send the email.
    try:
        # Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
    # Return an error if something goes wrong.
    except ClientError as e:
        return {
            'statusCode': '400',
            'body': "Amazon SES Error: " + e.response['Error']['Code'],
            'headers': {
                'Content-Type': 'application/json',
            },
        }
    else:
        return {
            'statusCode': '200',
            'body': "Message sent!",
            'headers': {
                'Content-Type': 'application/json',
            },
        }
# Phone number parsing
def parsephone(strphone):
    '''
    Pull out just the digits. Then do some simple formating.
    '''
    phn = ""
    for n in strphone:
        if n in "0123456789":
            phn += n
    if len(phn) == 10:  # add a 1 in front
        phn = "1" + phn
    if len(phn) != 11:
        return phn  # no hope of formating
    # format with dashes
    phn = "(" + phn[1:4] + ") " + phn[4:7] + "-" + phn[7:]
    return phn

# Lambda handler function:
# The first argument is the event object. An event is a JSON-formatted document
# that contains data from API Gateway for this Lambda function to process.
# The Lambda runtime converts the event to an object and passes it here.
def lambda_handler(event, context):
    # Load body of POST request, which has Flowroute SMS information
    b = json.loads(event['body'])
    # Filter for data and attributes, nested inside body.
    a = b['data']['attributes']
    # Format phone numbers
    fromnumber = parsephone(a['from'])
    tonumber = parsephone(a['to'])
    # SMS information is inside attributes, use it to send e-mail.
    return send_email('to@domain.com', 'from@domain.com', 'us-east-1', 'SMS from ' + fromnumber, fromnumber, tonumber, a['body'], a['timestamp'])
    

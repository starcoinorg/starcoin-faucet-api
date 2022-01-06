import boto3
from botocore.exceptions import ClientError
import os 
from app.core.config import settings
from loguru import logger

# make sure access key exits
# os.environ["AWS_ACCESS_KEY_ID"] = ""
# os.environ["AWS_SECRET_ACCESS_KEY"] = ""

# Create a new SES resource and specify a region.
client = boto3.client('ses',region_name=settings.AWS_REGION)

def batch_send(message):
    recv = settings.AWS_RECIPIENT.split(',')
    for email in recv:
        send(email, message)


def send(email, message):
    logger.info("send email: email={} message={}".format(email, message))
    # Replace sender@example.com with your "From" address.
    # This address must be verified with Amazon SES.
    SENDER = settings.AWS_SENDER

    # Replace recipient@example.com with a "To" address. If your account 
    # is still in the sandbox, this address must be verified.
    RECIPIENT = email

    # Specify a configuration set. If you do not want to use a configuration
    # set, comment the following variable, and the 
    # ConfigurationSetName=CONFIGURATION_SET argument below.
    CONFIGURATION_SET = ""

    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = settings.AWS_REGION

    # The subject line for the email.
    SUBJECT = settings.AWS_FAUCET_SUBJECT

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = ("\r\n"
                + message
                )
                
    # The HTML body of the email.
    BODY_HTML = """<html>
    <head></head>
    <body>
    <h1>{}</h1>
    <p>{}</p>
    </body>
    </html>
    """.format(settings.AWS_FAUCET_SUBJECT, message)       

    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Try to send the email.
    try:
        #Provide the contents of the email.
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
            # If you are not using a configuration set, comment or delete the
            # following line
            ConfigurationSetName=CONFIGURATION_SET,
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        logger.error("error: email={} message={}".format(email, e.response['Error']['Message']))
    else:
        logger.info("email sent!: MessageID={}".format(response['MessageId'])),
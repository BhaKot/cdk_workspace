import json


def lambda_handler(event, context):
    for record in event["Records"]:
        # Print the message body
        print("My Message Body: ", record["body"])

        # If you need to process any attributes
        if "messageAttributes" in record:
            print("Message Attributes: ", record["messageAttributes"])

    # TODO implement
    return {"statusCode": 200, "body": json.dumps("Hello from Lambda!")}

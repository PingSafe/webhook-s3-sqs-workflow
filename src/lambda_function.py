import json, hashlib, uuid, os
import boto3
import base64
import traceback


def sha256_hash(string):
    # Create a new SHA-256 hash object
    sha256 = hashlib.sha256()
    # Update the hash object with the bytes of the string
    sha256.update(string.encode())
    # Return the hexadecimal representation of the hash
    return sha256.hexdigest()

def lambda_handler(event, context):
    s3 = boto3.resource('s3')
    api_key = os.environ.get('PINGSAFE_API_KEY')
    bucket_name = os.environ.get('BUCKET_NAME')

    try:
        if event['requestContext']['http']['method'] != "POST":
            return {
                "statusCode": 405,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({
                    "error": "Method not allowed"
                })
            }
        body = json.loads(event['body'])
        headers = event['headers']

        # verify checksum
        if 'x-pingsafe-checksum' not in headers:
            print("X-PingSafe-Checksum header cannot be found, aborting request")
            return {
                "statusCode": 401,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({
                    "error": "cannot verify request"
                })
            }

        checksum = headers['x-pingsafe-checksum']
        # For more details refer to https://docs.pingsafe.com/getting-pingsafe-events-on-custom-webhook
        if sha256_hash(f"{body['event']}.{api_key}") != checksum:
            return {
                "statusCode": 403,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({
                    "error": "checksum verification failed"
                })
            }

        event_payload = base64.b64decode(body['event']).decode('utf-8')
        obj = s3.Object(bucket_name=bucket_name, key=f"{str(uuid.uuid4())}.json")
        response = obj.put(Body=event_payload)
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "message": response
            })
        }
    except Exception as error_message:
        print(traceback.format_exc())
        print("failed to accept event, error: ", error_message)
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "error": "failed to accept event, please check logs for more details"
            })
        }
#
# lambda_handler(event={
# 	"requestContext": {
# 		"http": {
# 			"method": "POST"
# 		}
# 	},
# 	"body": str({
# 			"event": "" // add base64 endcoded event
# 	}),
# 	"headers": {
# 		"x-pingsafe-checksum": "9a0e405373e6666fa7fb4ae60ff5f46934c91c2a6deca042deef567cd5452983"
# 	}
# }, context="")
import json
import boto3
import time
from botocore.exceptions import ClientError
# import re

AWS_S3BUCKET = 'ecor-rouge-work'
s3input_folder = 'Incoming'
s3output_folder = 'Processed'
CLIENT_S3 = boto3.client('s3')


def run(event, context):
    try:
        trigger_key = event['Records'][0]['s3']['object']['key']
    except (ValueError, KeyError) as e:
        print('error getting input file for processing:{}'.format(e))
        return {'status': 'error'}
    # # if necessary, you can further analyze the file for compliance with the pattern
    # if not re.match(s3input_folder+'/'+r'pattern\d{2}_end.json', trigger_key):
    #     message = 'the file {} does not match the pattern'.format(trigger_key)
    #     print(message)
    #     return {'status': message}
    input_json = get_json_from_s3(AWS_S3BUCKET, trigger_key)
    print('received file {}:'.format(trigger_key))
    print(json.dumps(input_json, indent=2))
    if isinstance(input_json, dict):
        input_json['processed_value'] = 'processed_value_{}'.format(int(time.time()))
    new_key = s3output_folder+'/' + '/'.join(trigger_key.split('/')[1:])
    if not save_s3_file(input_json, new_key):
        return {'status': 'error'}
    print('file {} processed and saved to folder {}'.format(trigger_key, s3output_folder))
    return {'status': 'ok'}


def get_json_from_s3(bucket, key):
    try:
        response = CLIENT_S3.get_object(Bucket=bucket, Key=key)
        body = response['Body']
        json_data = json.loads(body.read())
    except ClientError as e:
        print('{}:error getting file:{}'.format(key, e))
        return {}
    except ValueError as e:
        print('{}:error in json format:{}'.format(key, e))
        return {}
    except Exception as e:
        print('{}:unidentified error:{}'.format(key, e))
        return {}
    return json_data


def save_s3_file(body, key):
    try:
        _ = CLIENT_S3.put_object(Body=body,
                                 Bucket=AWS_S3BUCKET,
                                 Key=key)
    except ClientError as e:
        print('error saving file {}:{}'.format(key, e))
        return False
    return True


if __name__ == '__main__':
    test_key = '123.json'
    event_emu = {'Records': [{'s3': {'object': {'key': test_key}}}]}
    run(event_emu, '')

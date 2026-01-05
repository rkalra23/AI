import json
#1. import boto3
import boto3
import base64
import datetime
#2. Create client connection with Bedrock and S3 Services – Link
client_bedrock = boto3.client('bedrock-runtime',region_name="us-west-2")
client_s3 = boto3.client('s3')

def lambda_handler(event, context):
    #3. Store input i.e. prompt in variable
    input_prompt=event['prompt']
    print(input_prompt)
    #4. Create a Request Syntax to access the Bedrock Service 
    response_bedrock = client_bedrock.invoke_model(contentType='application/json', accept='application/json',modelId='stability.sd3-5-large-v1:0',
       body=json.dumps({
        'prompt': input_prompt
    })
    )
    #print(response_bedrock)
    response_bedrock_byte=json.loads(response_bedrock['body'].read().decode("utf-8"))
    print(response_bedrock_byte)
    #6. 6a. Retrieve data with artifact key, 6b. Import Base 64, 6c. Decode from Base64
    response_bedrock_base64 = response_bedrock_byte['images'][0]
    response_bedrock_finalimage = base64.b64decode(response_bedrock_base64)
    # print(response_bedrock_finalimage)
    #7a. Upload the File to S3 using Put Object Method – Link 7b. Import datetime 7c. Generate the image name to be stored in S3 - Link
    poster_name = 'posterName'+ datetime.datetime.today().strftime('%Y-%M-%D-%M-%S')
    
    response_s3=client_s3.put_object(
        Bucket='YourBucketname',
        Body=response_bedrock_finalimage,
        Key=poster_name)

#8. Generate Pre-Signed URL 
    generate_presigned_url = client_s3.generate_presigned_url('get_object', Params={'Bucket':'YourBucketname','Key':poster_name}, ExpiresIn=3600)
    # print(generate_presigned_url)
    return {
        'statusCode': 200,
        'body': generate_presigned_url
    }


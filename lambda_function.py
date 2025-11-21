import json
import boto3
import os
import io
from PIL import Image
#I got the pillow python API and uploaded it as a layer for this to work

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # We configure the buckets here 
    SOURCE_BUCKET = 'capstone-images-original'
    DEST_BUCKET = 'capstone-images-resized'
    
    # 1. Parses input from Step Functions
    key = event.get('key')
    if not key:
        return {'status': 'fail', 'error': 'No key provided'}
    
    try:
        # 2. Gets the image from S3
        response = s3.get_object(Bucket=SOURCE_BUCKET, Key=key)
        image_content = response['Body'].read()
        
        # 3. Resizes the  image
        with Image.open(io.BytesIO(image_content)) as img:
            img.thumbnail((128, 128))
            buffer = io.BytesIO()
            img.save(buffer, 'JPEG')
            buffer.seek(0)
            
            # 4. Uploads the resized image
            resized_key = f"resized-{key}"
            s3.put_object(Bucket=DEST_BUCKET, Key=resized_key, Body=buffer)
            
        return {'status': 'success', 'original': key, 'resized': resized_key}
        
    except Exception as e:
        return {'status': 'fail', 'error': str(e)}
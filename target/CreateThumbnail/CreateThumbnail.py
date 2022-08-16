# lambda_function.py
import boto3
from io import BytesIO
from os import path
from PIL import Image
     
s3 = boto3.resource('s3')
INCOMING_BUCKET     = 'filebucket78273ueoiqwdadui'
DESTINATION_BUCKET  = 'filebucket78273ueoiqwdadui'
     
def lambda_handler(event, context):
    for key in event.get('Records'):
        object_key = key['s3']['object']['key']
        extension = path.splitext(object_key)[1].lower()

        # Grabs the source file
        obj = s3.Object(
            bucket_name=INCOMING_BUCKET,
            key=object_key,
        )
        obj_body = obj.get()['Body'].read()
    
        # Checking the extension and
        # Defining the buffer format
        if extension in ['.jpeg', '.jpg', '.png']:
            format = 'JPEG'

        # Image resize
        image = Image.open(BytesIO(obj_body))
        output_size = (1000, 1000)
        image.thumbnail(output_size) # image.thumbnail preserves aspect ratio, does does not exceed specified size, 
        buffer = BytesIO()
        image.save(buffer, format)
        buffer.seek(0)

        # Upload resized image to destination bucket
        obj = s3.Object(
            bucket_name=DESTINATION_BUCKET,
            key=f"{object_key}",
        )
        obj.put(Body=buffer)

        # Print to CloudWatch
        print('File saved at {}/{}'.format(
            DESTINATION_BUCKET,
            object_key,
        ))
        print("Image resize lambda handler completed.")
import boto3
import os
import sys
import uuid
from PIL import Image
import PIL.Image
     
s3_client = boto3.client('s3')
     
def resize_image(image_path, resized_path):
    with Image.open(image_path) as image:
        image.thumbnail((128, 128))
        image.save(resized_path)
     
def handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key'] 
        download_path = '/tmp/{}{}'.format(uuid.uuid4(), key)
        upload_path = '/tmp/resized-{}'.format(key)
        
        s3_client.download_file(bucket, key, download_path)
        resize_image(download_path, upload_path)
        s3_client.upload_file(upload_path, '{}-resized'.format(bucket), key)



def copy_to_other_bucket(src, des, key):
    try:
        copy_source = {
            'Bucket': src,
            'Key': key
        }
        bucket = s3.Bucket(des)
        bucket.copy(copy_source, key)
    except Exception as e:
        print(e)


def resize_image(src_bucket, des_bucket):
    size = 500, 500
    bucket = s3.Bucket(src_bucket)
    in_mem_file = BytesIO()
    client = boto3.client('s3')

    for obj in bucket.objects.all():
        file_byte_string = client.get_object(Bucket=src_bucket, Key=obj.key)['Body'].read()
        im = Image.open(BytesIO(file_byte_string))

        im.thumbnail(size, Image.ANTIALIAS)
        im.save(in_mem_file, format=im.format)
        in_mem_file.seek(0)

        response = client.put_object(
            Body=in_mem_file,
            Bucket=des_bucket,
            Key='resized_' + obj.key
        )

def handler(event, context):
    bucket = s3.Bucket('test8371036')

    for obj in bucket.objects.all():
        copy_to_other_bucket(bucket, 'test8371036-resized', obj.key)

    resize_image(bucket.name, 'test8371036')


    print(bucket)


import boto3
import csv
from datetime import datetime

def lambda_handler(event, context):
    s3_client = boto3.client('s3', endpoint_url="http://localhost:4566")
    dynamodb_client = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")
    
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    response = s3_client.get_object(Bucket=bucket, Key=key)
    content = response['Body'].read().decode('utf-8').splitlines()

  
    csv_reader = csv.reader(content)
    rows = list(csv_reader)
    row_count = len(rows) - 1
    column_names = rows[0]
    column_count = len(column_names)
    
    
    metadata = {
        'filename': key,
        'upload_timestamp': str(datetime.now()),
        'file_size_bytes': response['ContentLength'],
        'row_count': row_count,
        'column_count': column_count,
        'column_names': column_names
    }
    
    table = dynamodb_client.Table('FileMetadataTable')
    table.put_item(Item=metadata)

    return {"statusCode": 200, "body": "Metadata stored successfully!"}

import pdb
import os 

import boto3

from libs.configs import SD_BUKET_NAME, SD_OUTPUT_PATH




# 파일 업로드
def upload_file(file_path, key_name):
    target_path = os.path.join(SD_OUTPUT_PATH, key_name)
    
    s3 = boto3.client('s3')
    
    s3.upload_file(file_path, SD_BUKET_NAME, target_path)
    
    print(f"File '{file_path}' uploaded to S3 bucket '{SD_BUKET_NAME}' with key '{target_path}'")

# JSON 문자열을 S3에 업로드
def upload_json_string(json_str, key_name):
    target_path = os.path.join(SD_OUTPUT_PATH, key_name)
    
    s3 = boto3.client('s3')
    s3.put_object(Body=json_str, Bucket=SD_BUKET_NAME, Key=target_path)
    print(f"JSON data uploaded to S3 bucket '{SD_BUKET_NAME}' with key '{key_name}'")


# 파일 다운로드
def download_file(file_path, s3_path):
    if not s3_path:
        return
    
    s3 = boto3.client('s3')
    
    s3.download_file(SD_BUKET_NAME, s3_path, file_path)
    
    print(f"S3 file '{s3_path}' from bucket '{SD_BUKET_NAME}' downloaded to '{file_path}'")


import pdb
import os 

import boto3
from dotenv import load_dotenv

# load .env
load_dotenv()


# S3 버킷 이름 및 키 (파일 이름)
bucket_name = 'covis-gnosis'
key_name = 'data/hsb/datasets/stable_diffusion_data/chatgpt_gen/hsd_onepiece_0.json'
pdb.set_trace()
# S3 클라이언트 생성
s3 = boto3.client('s3')

# 파일 업로드
def upload_file(file_path, bucket_name, key_name):
    s3.upload_file(file_path, bucket_name, key_name)
    print(f"File '{file_path}' uploaded to S3 bucket '{bucket_name}' with key '{key_name}'")

file_path = 'training/text_to_image/tools//hsd_onepiece_0.json'
upload_file(file_path, bucket_name, key_name)

# # 파일 다운로드
def download_file(file_path, bucket_name, key_name):
    s3.download_file(bucket_name, key_name, file_path)
    print(f"S3 file '{key_name}' from bucket '{bucket_name}' downloaded to '{file_path}'")

download_file_path = 'path/to/your/downloaded_file.ext'
download_file(download_file_path, bucket_name, key_name)

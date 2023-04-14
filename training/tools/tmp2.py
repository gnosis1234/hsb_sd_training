import os
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

# 인증 및 API 클라이언트 생성
def create_drive_api_client():
    SCOPES = ['https://www.googleapis.com/auth/drive']
    CLIENT_SECRET_FILE = 'client_secrets.json'

    creds = None
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
    creds = flow.run_local_server(port=8080)

    try:
        service = build('drive', 'v3', credentials=creds)
        return service
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None

# 파일 업로드 함수
def upload_to_drive(service, file_path, file_name, parent_folder_id=None):
    file_metadata = {'name': file_name}
    if parent_folder_id:
        file_metadata['parents'] = [parent_folder_id]

    media = MediaFileUpload(file_path, resumable=True)
    try:
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(F'File ID: "{file.get("id")}".')
        return file
    except HttpError as error:
        print(F"An error occurred: {error}")
        return None

if __name__ == "__main__":
    # Google Drive API 클라이언트 생성
    service = create_drive_api_client()

    # 업로드할 파일의 경로와 이름 설정
    file_path = 'hsd_onepiece_1.json'  # 업로드할 파일의 경로와 이름을 지정하세요.
    file_name = 'hsd_onepiece_1.json'  # 구글 드라이브에 저장될 파일의 이름을 지정하세요.
    parent_folder_id = '1L4TaIks4IuvYITOoWBfk_lwz4FVdn6RR'  # 필요한 경우 상위 폴더의 ID를 지정하세요. 그렇지 않으면 루트 디렉토리에 업로드됩니다.

    # 파일 업로드
    upload_to_drive(service, file_path, file_name, parent_folder_id)


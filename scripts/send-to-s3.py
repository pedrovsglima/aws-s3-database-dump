from datetime import datetime
import boto3
import os

def get_credentials(file):
    with open(file, 'r') as f:
        KEY_ID = f.readline().strip()
        ACCESS_KEY = f.readline().strip()
        BUCKET_NAME = f.readline().strip()

    return KEY_ID, ACCESS_KEY, BUCKET_NAME


class AWSobjectWrapper:

    def __init__(self, s3_object):
        self.object = s3_object

    def create_bucket_if_necessary(self, s3_bucket):
        self.bucket_name = s3_bucket
        
        existing_buckets = [bucket['Name'] for bucket in self.object.list_buckets()['Buckets']]
       
        if self.bucket_name not in existing_buckets: 
            self.object.create_bucket(Bucket=self.bucket_name)
    
    def count_files_in_folder(self):
        self.files_per_day = 0
        
        existing_files = self.object.list_objects(Bucket=self.bucket_name)

        if 'Contents' in existing_files:
            self.files_per_day = sum(1 for content in existing_files.get('Contents') \
                                            if current_date in content.get('Key'))

    def message_log_file(self, message):
        with open(log_file, 'a+') as file:
            file.write(f"{current_date},{current_hour},{message}\n")
    
    def upload_dump_file(self, source_file):
        self.count_files_in_folder()

        try:
            self.object.upload_file(
                    Filename=source_file,
                    Bucket=self.bucket_name,
                    Key=f'{current_date}/datadump{self.files_per_day + 1}.sql'
                    )

        except Exception as e:
            self.message_log_file(e)

        else:
            self.message_log_file('file successfully uploaded')
            os.remove(source_file)
        

def main():

    KEY_ID, ACCESS_KEY, BUCKET_NAME = get_credentials('../credentials.txt')
    
    s3 = boto3.client('s3', region_name='us-east-1',
                  aws_access_key_id=KEY_ID,
                  aws_secret_access_key=ACCESS_KEY)
    
    send_dump_file = AWSobjectWrapper(s3)

    send_dump_file.create_bucket_if_necessary(BUCKET_NAME)     

    send_dump_file.upload_dump_file(DUMP_FILE)


if __name__ == '__main__':
    
    DUMP_FILE = '/dumps/datadump.sql'

    current_date = datetime.today().strftime("%Y-%m-%d")
    current_hour = datetime.today().strftime("%H:%M:%S")
    log_file = f"../logs/{current_date}.txt"
    
    if os.path.exists(DUMP_FILE):
        main()

    else:
        with open(log_file, 'a+') as file:
            file.write(f"{current_date},{current_hour},there is no file to upload\n")
import boto3
from get_bucket_name import get_bucket_name

def upload_csv_to_s3(file_path, bucket_name, key):
    s3 = boto3.client('s3')
    s3.upload_file(file_path, bucket_name, key)
    print(f"✅ Uploaded {file_path} to s3://{bucket_name}/{key}")

if __name__ == "__main__":
    STACK_NAME = "north-agent-stack"
    LOGICAL_BUCKET_ID = "StressCSVBucket"
    FILE_PATH = "data/university_mental_health_iot_dataset.csv"
    S3_KEY = "stress-raw.csv"

    # Get bucket name dynamically
    bucket_name = get_bucket_name(STACK_NAME, LOGICAL_BUCKET_ID)

    # Upload the CSV
    upload_csv_to_s3(FILE_PATH, bucket_name, S3_KEY)


import boto3

def upload_csv_to_s3(file_path, bucket_name, key):
    s3 = boto3.client('s3')
    s3.upload_file(file_path, bucket_name, key)
    print(f"Uploaded {file_path} to s3://{bucket_name}/{key}")

if __name__ == "__main__":
    upload_csv_to_s3(
        "data/university_mental_health_iot_dataset.csv",
        "placeholder-bucket-name",
        "stress-raw.csv"
    )

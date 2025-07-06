import csv
import boto3
from datetime import datetime
from db import store_user_data_batch, convert_row_to_item
from model import compute_stress_score, is_high_stress

def lambda_handler(event, context):
    s3 = boto3.client("s3")
    items_to_write = []

    try:
        bucket = event["Records"][0]["s3"]["bucket"]["name"]
        key = event["Records"][0]["s3"]["object"]["key"]
        print(f"Processing file s3://{bucket}/{key}")

        obj = s3.get_object(Bucket=bucket, Key=key)
        lines = obj["Body"].read().decode("utf-8").splitlines()
        reader = csv.DictReader(lines)

        user_counter = 1
        total_rows = 0
        high_stress_count = 0

        for row in reader:
            total_rows += 1

            # Ensure required fields are present
            if not all(field in row and row[field] for field in ("timestamp", "stress_level", "sleep_hours", "mood_score")):
                print(f"Skipping row {total_rows}: missing fields → {row}")
                continue

            # Compute score once
            score = compute_stress_score(row)
            print(f"Row {total_rows} → score: {score} | data: {row}")

            if not is_high_stress(score):
                continue

            high_stress_count += 1

            # Parse timestamp
            try:
                raw_timestamp = row["timestamp"]
                timestamp = datetime.strptime(raw_timestamp, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%dT%H:%M:%SZ")
            except Exception as e:
                print(f"Skipping row {total_rows}: invalid timestamp → {raw_timestamp} ({e})")
                continue

            user_id = f"user-{user_counter:03d}"
            user_counter += 1

            row["stress_score"] = score
            item = convert_row_to_item(user_id, timestamp, row, stress_score=score)
            items_to_write.append(item)

        print(f"Total rows read: {total_rows}")
        print(f"High stress rows: {high_stress_count}")
        print(f"Prepared {len(items_to_write)} items for DynamoDB")

        if items_to_write:
            store_user_data_batch(items_to_write)
        else:
            print("No items to store in DynamoDB")

        return {
            "statusCode": 200,
            "body": f"Successfully processed {len(items_to_write)} users"
        }

    except Exception as e:
        print(f"Lambda error: {e}")
        return {
            "statusCode": 500,
            "body": f"Error: {str(e)}"
        }

import boto3
import os
from decimal import Decimal, InvalidOperation

dynamodb = boto3.resource("dynamodb")
table_name = os.getenv("DDB_TABLE", "HighStressUsers")
table = dynamodb.Table(table_name)

def store_user_data_batch(items):
    try:
        with table.batch_writer() as batch:
            for item in items:
                print(f"Writing to DynamoDB: {item}")
                batch.put_item(Item=item)
        print(f"Successfully wrote {len(items)} items to DynamoDB table {table_name}")
    except Exception as e:
        print(f"Error writing batch to DynamoDB: {e}")
        raise

def convert_row_to_item(user_id, timestamp, row, stress_score=None):
    item = {
        "user_id": user_id,
        "timestamp": timestamp,
    }

    for key, value in row.items():
        if key == "timestamp":
            continue
        if value is None or value == "":
            continue
        try:
            item[key] = Decimal(str(value))
        except (InvalidOperation, ValueError):
            item[key] = str(value)

    # Ensure stress_score is included
    if stress_score is not None:
        item["stress_score"] = Decimal(str(stress_score))

    return item

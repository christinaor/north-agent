import boto3
import os
from boto3.dynamodb.conditions import Key, Attr
from decimal import Decimal
import json

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.getenv("DDB_TABLE", "HighStressUsers"))

def lambda_handler(event, context):
    try:
        # Scan for stress_score >= 0.4
        response = table.scan(
            FilterExpression=Attr("stress_score").gte(Decimal("0.4"))
        )

        alerts = []
        for item in response.get("Items", []):
            alerts.append({
                "user_id": item["user_id"],
                "stress_score": float(item["stress_score"]),
                "timestamp": item["timestamp"]
            })

        return {
            "statusCode": 200,
            "body": json.dumps(alerts)
        }

    except Exception as e:
        print(f"[ERROR] {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

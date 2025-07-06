def lambda_handler(event, context):
    for record in event['Records']:
        if record['eventName'] in ('INSERT', 'MODIFY'):
            new_image = record['dynamodb']['NewImage']
            user_id = new_image['user_id']['S']
            stress_score = float(new_image.get('stress_score', {}).get('N', '0'))
            timestamp = new_image['timestamp']['S']

            # Example: Log or send notifications here
            print(f"ALERT: High stress user {user_id} with score {stress_score} at {timestamp}")

    return {"status": "processed"}

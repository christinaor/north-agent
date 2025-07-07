import boto3

def get_bucket_name(stack_name: str, logical_id: str) -> str:
    cf = boto3.client("cloudformation")
    resources = cf.describe_stack_resources(StackName=stack_name)

    for res in resources["StackResources"]:
        if res["LogicalResourceId"] == logical_id and res["ResourceType"] == "AWS::S3::Bucket":
            return res["PhysicalResourceId"]

    raise Exception(f"Bucket with Logical ID '{logical_id}' not found in stack '{stack_name}'.")

if __name__ == "__main__":
    STACK_NAME = "north-agent-stack"
    LOGICAL_BUCKET_ID = "StressCSVBucket"

    bucket_name = get_bucket_name(STACK_NAME, LOGICAL_BUCKET_ID)
    print(bucket_name)

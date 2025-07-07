# north-agent

## Objective

The goal is to create an autonomous agent pipeline to detect high-stress students and store alerts when these students are found in a dataset. For the purposes of this exercise, data on students with a stress threshold of 0.4 and above will be included.

## Directory Structure

```bash
serverless-app/
├── template.yaml
├── py-lambda/
│ ├── db/
│ │ ├── __init__.py
│ │ ├── handler.py
│ │ ├── model.py
│ │ ├── requirements.txt
│ │ └── utils/
│ │ ├── __init__.py
│ │ └── process_db.py
│ ├── alert-processor/
│ │ ├── __init__.py
│ │ ├── handler.py
│ │ └── requirements.txt
│ └── api/
│ ├── __init__.py
│ ├── handler.py
│ └── requirements.txt
├── requirements.txt
├── setup.py
└── samconfig.toml
```

## Tech Stack

-   Python 3
-   AWS Services
    -   **Lambda**: Functions running the pipeline
    -   **S3**: Ingest CSV data
    -   **DynamoDB**: Key-value database for processed stress data and alerts
    -   **API Gateway**: Exposes GET endpoint for alerts
    -   **CloudWatch**: Logging to monitor pipeline health and errors

## Install packages:

Navigate to serverless-app and install packages:

```bash
pip install -e
```

## Architecture

For each AWS Service, configurations and user policies will need to be set in the corresponding service and IAM platform before the lambda functions can run and data storing services can be used. Cloudwatch was used to check whether functions were active and running correctly.

## Model for DB data

Keeping it simple by creating a light heuristic model. The stress score determines whether they are at or above the threshold and is weighted on the students' stress level, number of sleep hours, and mood.

## Running the pipeline

An AWS user should have permissions for reading and getting objects from S3 buckets and writing to DynamoDB. The lambda should have AWSLambdaBasicExecutionRole as well as getting objects from S3 buckets. Policies can be updated in IAM.

Validate the YAMLs:

```bash
sam validate
```

Build the stack:

```bash
sam build
```

Deploy the stack with a guide (samconfig.toml).

```bash
sam deploy --guided
```

**WORKAROUND NEEDED**: There is a circular dependency across the AWS services using the bucket name in template.yaml, so deployment will need to be done twice (once for bucket creation, once more for updating lambdas).

Find the bucket name:

```bash
python3 scripts/get_bucket_name.py
```

In template.yaml and upload_csv.py, update "placeholder-bucket-name" with the response from the previous command.

Rerun the build and deploy commands after saving. The north-agent-stack should now be deployed.

### Triggering the pipeline

Start the pipeline by adding a CSV file to the S3 bucket. It can either be manually added through the console or by using a command in the terminal:

```bash
python3 scripts/upload_csv.py
```

### Check DynamoDB for table of high stress students

The data in the table can inspected and filtered for stress_score using the AWS CLI. Commands can also be run to view the data:

```bash
aws dynamodb scan \
 --table-name HighStressUsers \
 --region us-east-1
```

### Accessing the GET API

In the API Gateway console, the endpoint can be found where high stress users will be located as as JSON. Navigate to **Stages** > ** Prod** > /alerts endpoint. The JSON will be in this format:

```bash
[
  {
    "user_id": "user-001",
    "stress_score": 0.83,
    "timestamp": "2025-05-22T00:00:00Z"
  }
]
```

Todo: Look into AWS ML services.

# Serverless Image Processing Capstone

## Project Overview
This project is a serverless application that automatically resizes images uploaded to AWS. It utilizes **API Gateway** to trigger a workflow, **Step Functions** for orchestration, and **AWS Lambda** (with a custom Pillow library layer) for image processing, storing the results in **Amazon S3**.

## Architecture
<img width="1912" height="1067" alt="Screenshot 2025-11-21 011046" src="https://github.com/user-attachments/assets/a2fc4451-96b8-4a30-832e-4c9790412a7d" />


The pipeline flow:
1.  **API Gateway** receives a request.
2.  **Step Functions** coordinates the workflow.
3.  **Lambda** fetches the image from the Source Bucket, resizes it, and saves it to the Destination Bucket.
4.  **S3** stores the final thumbnail.

## Prerequisites
* Active AWS Account.
* **Pillow Layer Zip:** A custom Lambda Layer zip file containing the `Pillow` library (uploaded as `pillow_layer.zip`).

## Deployment Instructions

### 1. Storage (S3)
Create two S3 buckets with unique names:
* **Source:** `capstone-original-images`
* **Destination:** `capstone-resized-images`

### 2. Compute (Lambda)
* **Create Layer:** Generate the layer locally on your computer using the pip install command at the bottom of this post

Upload the `pillow_layer.zip` file to the AWS Lambda Console as a new Layer.
* **Create Function:** Create a Python 3.x function named `ImageResizer`.
* **Attach Layer:** Add the custom Pillow layer to the function configuration.
* **Permissions:** Attach an IAM Role with permissions to read/write to S3 and write to CloudWatch Logs.
* **Deploy Code:** Deploy the code found in `lambda_function.py`.

### 3. Orchestration (Step Functions)
* Create a standard State Machine.
* Copy the JSON definition from `workflow.json`  
* Update the `Resource` ARN in the JSON to match your Lambda function's ARN.

### 4. Trigger (API Gateway)
* Create a REST API with a `POST` method.
* Integrate it with **Step Functions** -> `StartExecution`.
* Apply the **VTL Mapping Template** to pass the input correctly.
* Deploy the API to a stage (e.g., `prod`).

## Usage
To trigger the pipeline, send a POST request to your API Invoke URL:

```bash
pip install Pillow --platform manylinux2014_x86_64 --target=python/ --implementation cp --python-version 3.12 --only-binary=:all: --upgrade pillow 


```bash
curl -X POST [https://YOUR-API-ID.execute-api.us-east-1.amazonaws.com/prod/process](https://YOUR-API-ID.execute-api.us-east-1.amazonaws.com/prod/process) \
-H "Content-Type: application/json" \
-d '{"key": "test-image.jpg"}'


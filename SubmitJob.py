#!/usr/bin/env python3

def submit_job(event, context):
    """Triggered by a change to a Cloud Storage bucket.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    import requests
    import random
    file = event
    print(f"File modified: {file['name']}.")
    job_id = f'updated_files_in_bucket_{random.randint(0,99999)}'
    print (job_id)  #remove this later
    data = {
        "projectId": "spark-project3",
        "job": {
            "placement": {
                "clusterName": "spark-project3"
            },
            "reference": {
                "jobId":  job_id
            },
            "pysparkJob": {
                "mainPythonFileUri": "gs://input_spark/test_df_spark.py",
                "args": [
                    "gs://input_spark/iris.csv",
                    "gs://output_spark"
                ]
            }
        }
    }
    url = "v1/projects/spark-project3/regions/us-east1/jobs:submit/"
    requests.post(url=url, data=data)

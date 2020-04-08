# Cloud_Computing_Project_3
Cloud Map Reduce and Distributed Jobs

Set enviromental variables
```bash
export REGION=`Region you prefer`
export PROJECT_ID=`Insert Project ID`
export CLUSTER_REGION=`Region you prefer`
export CLUSTER=`Name you prefer `
```

Create buckets
```bash
gsutil mb -p $PROJECT_ID -l $REGION -b on gs://input_spark/
gsutil mb -p $PROJECT_ID -l $REGION -b on gs://output_spark/
```

Add file to bucket
```bash
gsutil cp iris.csv gs://input_spark/iris.csv
```

Create cluster
```bash
gcloud dataproc clusters create $CLUSTER \
    --region=$REGION \
    --project=$PROJECT_ID \
    --single-node
```

Submit job to cluster    
```bash
gcloud dataproc jobs submit pyspark test_df_spark.py  \
    --cluster=$CLUSTER \
    --region=$REGION  \
    -- gs://input_spark/iris.csv gs://output_spark
 ```
 
 Do this manually using the GUI
 ```bash
 gsutil cp test_df_spark.py gs://input_spark/test_df_spark.py
```


#Submit job using POST request
https://cloud.google.com/dataproc/docs/guides/submit-job
Check the NOTE where it mentions how can you get the Equivalent REST request on the GUI
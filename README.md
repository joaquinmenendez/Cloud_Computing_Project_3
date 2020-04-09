# Cloud_Computing_Project_3
Cloud Map Reduce and Distributed Jobs

**Previous projects**<br>
[Docker containerization](https://github.com/joaquinmenendez/Cloud_Computing_Project_2)<br>
[Continuous Delivery of Flask Application on GCP](https://github.com/joaquinmenendez/Cloud_Computing_Project_1)<br>
**Next projects**<br>
[Using Google Cloud Services to develop a Serverless Data Engineering Pipeline](https://github.com/joaquinmenendez/Cloud_Computing_Project_4)


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
gcloud dataproc jobs submit pyspark test_df_spark_v2.py  \
    --cluster=$CLUSTER \
    --region=$REGION  \
    -- gs://input_spark/iris.csv gs://output_spark
 ```
 
 Do this manually using the GUI<br>
 First, we copy the script into a bucket. In this case we are going to use `input_spark` 
 ```bash
 gsutil cp test_df_spark_v2.py gs://input_spark/test_df_spark_v2.py
```
![]()

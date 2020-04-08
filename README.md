# Cloud_Computing_Project_3
Cloud Map Reduce and Distributed Jobs


export REGION=`Region you prefer`
export PROJECT_ID=`insert Project ID`
export CLUSTER_REGION=us-east1
export CLUSTER=spark-project3

#buckets
gsutil mb -p $PROJECT_ID -l $REGION -b on gs://input_spark/
gsutil mb -p $PROJECT_ID -l $REGION -b on gs://output_spark/

#cluster
gcloud dataproc clusters create $CLUSTER \
    --region=$REGION \
    --project=$PROJECT_ID \
    --single-node
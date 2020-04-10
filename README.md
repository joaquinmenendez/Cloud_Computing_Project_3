# Submitting a Pyspark job to a Spark cluster on GCP
## Data Analysis in the Cloud at Scale (ECE 590.24) - Project 3

This is a tutorial of how to create a cluster and submit a Pyspark job in GCP. This tutorial also explain how to store these outputs into a bucket. You can see a video demostration [here]()

What are we going to do in this tutorial
- Create a Spark cluster on GCP
- Submit a job to this cluster
- Store the output of this job into a bucket.

On the repo, you will find two different Pyspark jobs: `test_df_spark_v2.py` and `test_df_spark.py`.  `test_df_spark_v2.py` will do several things. First, it will read a file from a bucket (`iris.csv`) and using the `pyspark.SQL` module it will print out a simple show statement with the first 10 observations. Secondly, it will print out the observation with the maximum sepal_length grouped by type of flower and will save the output into a bucket. After this, it will train a simple logistic regression using the `pyspark.ML` module. It will print out the coefficients and the accuracy of the model and will store the model into a bucket.

This could be included into a bigger pipeline. For example, you can also create a [Cloud Function](https://github.com/joaquinmenendez/Cloud_Computing_Project_4) to trigger a process after the outputs are stored in the bucket. 

**Previous projects**<br>
- [Docker containerization](https://github.com/joaquinmenendez/Cloud_Computing_Project_2)<br>
- [Continuous Delivery of Flask Application on GCP](https://github.com/joaquinmenendez/Cloud_Computing_Project_1)<br>
**Next projects**<br>
- [Using Google Cloud Functions to develop a Serverless Data Engineering Pipeline](https://github.com/joaquinmenendez/Cloud_Computing_Project_4)
---

First start cloning this repository on your project
```bash
#HTTP
git clone https://github.com/joaquinmenendez/Cloud_Computing_Project_3.git
#SSH
git clone git@github.com:joaquinmenendez/Cloud_Computing_Project_3.git
```

Set the enviromental variables. I reccomend creating a bash file like `env_variables.sh` in order to save your configuration.
```bash
export REGION=`Region you prefer`
export PROJECT_ID=`Insert Project ID`
export CLUSTER_REGION=`Region you prefer`
export CLUSTER=`Name you prefer `
```

Create  some buckets. In our case we are going to creat two, one for inputs and other for outputs. This is completely arbitrary, you can store all the files in one bucket if you want.
```bash
gsutil mb -p $PROJECT_ID -l $REGION -b on gs://input_spark/
gsutil mb -p $PROJECT_ID -l $REGION -b on gs://output_spark/
```

Add files to buckets. In this case we will add the classic Iris data set and our Pyspark job.
```bash
gsutil cp iris.csv gs://input_spark/iris.csv
gsutil cp test_df_spark_v2.py gs://input_spark/test_df_spark_v2.py
```

Let's create a Spark cluster using the console
```bash
gcloud dataproc clusters create $CLUSTER \
    --region=$REGION \
    --project=$PROJECT_ID \
    --single-node
```

Submit a job to cluster. We are going to set two argument or variables `gs://input_spark/iris.csv` and `gs://output_spark`. Our pyspark job is going to use this two argument to read and store our data. It is not necesary to pass arguments to a Pyspark job, but is a good idea to write flexible code in order to been able to use it againg the future.

```bash
gcloud dataproc jobs submit pyspark test_df_spark_v2.py  \
    --cluster=$CLUSTER \
    --region=$REGION  \
    -- gs://input_spark/iris.csv gs://output_spark
 ```
 Now if we go to the logs of our job we could observe the output.
 ![Job Log](https://user-images.githubusercontent.com/43391630/78952467-9ff34680-7aa3-11ea-8b45-9984cc375cd5.png)
 
 Also, we can see that now we have new files in our output bucket.
 ![Bucket outpu](https://user-images.githubusercontent.com/43391630/78952861-e85f3400-7aa4-11ea-84bb-ea997d960f6d.png
 
 You can create a cluster manually using the GUI. We need to go to Datapoc/clusters and click on 'Create a new cluster'<br>
 ![Create](https://user-images.githubusercontent.com/43391630/78735282-6510d780-7918-11ea-9800-b69b82b82d2a.png)
 
  
 You can submit a job to aclaster manually using the GUI<br> 
 To do so, set the following configuration:
  ![Configuration](https://user-images.githubusercontent.com/43391630/78744927-d6f51b00-7930-11ea-8aab-e496fbc46b5f.png)
  
  


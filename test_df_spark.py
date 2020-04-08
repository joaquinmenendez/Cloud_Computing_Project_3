#!/usr/bin/env python
import sys
from pyspark.sql import SparkSession
spark = SparkSession.builder.getOrCreate()

if len(sys.argv) != 3:
  raise Exception("Exactly 2 arguments are required: <input_bucket> <output_bucket>")

input_bucket = sys.argv[1]
output_bucket = sys.argv[2]
print("Reading file = {}".format(input_bucket))  # Testing that is working

df = (
    spark.read.
    format('csv').
    option('header', 'true').
    option('inferSchema', 'true').
    load(input_bucket)
)

df.createOrReplaceTempView('df_table') #create temp folder using the Pyspark SQL functions
spark.sql('''SELECT * FROM df_table''').show(5) #print the first 5 rows

query = spark.sql('''SELECT * FROM df_table LIMIT 5''') #Using LIMIT instead of show
query.write.save(sys.argv[2] + '/Query_Iris', format="json")
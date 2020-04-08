#!/usr/bin/env python
import sys
from pyspark.sql import SparkSession
spark = SparkSession.builder.getOrCreate()

if len(sys.argv) != 3:
  raise Exception("Exactly 2 arguments are required: <input_bucket> <output_bucket>")

input_bucket = sys.argv[1]
output_bucket = sys.argv[2]
df = spark.createDataFrame(input_bucket)
print(df.head())
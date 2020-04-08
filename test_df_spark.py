#!/usr/bin/env python
import sys
from pyspark.sql import SparkSession
spark = SparkSession.builder.getOrCreate()

if len(sys.argv) != 3:
  raise Exception("Exactly 2 arguments are required: <input_bucket> <output_bucket>")

input_bucket = sys.argv[1]
output_bucket = sys.argv[2]
print(input_bucket) #testing that is working

df = (
    spark.read.
    format('csv').
    option('header', 'true').
    option('inferSchema', 'true').
    load(input_bucket)
)
print(df.head())
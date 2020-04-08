#!/usr/bin/env python
import sys
from pyspark.sql import SparkSession
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.feature import StandardScaler
from pyspark.ml.feature import VectorAssembler

from datetime import datetime

date = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')

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

#Plot the means group by variety
spark.sql('''SELECT AVG(sepal.length, sepal.width,petal.length, petal.width) FROM df_table GROUP BY variety''').show()

#ML
#Pre-process the data
assembler = VectorAssembler(
    inputCols=['sepal.length', 'sepal.width','petal.length','petal.width'],
    outputCol="raw_features")
vector_df = assembler.transform(df)

# Scale features to have zero mean and unit standard deviation
standarizer = StandardScaler(withMean=True, withStd=True,
                              inputCol='raw_features',
                              outputCol='features')
model = standarizer.fit(vector_df)
vector_df = model.transform(vector_df)

# Convert label to number
indexer = StringIndexer(inputCol="raw_label", outputCol="label")
indexed = indexer.fit(vector_df).transform(vector_df)

indexed.show(10)

#LR
#lr = LogisticRegression(labelCol="label", featuresCol="features", maxIter=10)


#query.write.save(sys.argv[2] + '/Query_Iris_' + str(date), format="json")
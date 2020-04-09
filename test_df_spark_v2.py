#!/usr/bin/env python
import sys
import os
from pyspark.sql import SparkSession
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.feature import StandardScaler
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.feature import StringIndexer
import warnings
from datetime import datetime
import pickle

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
spark.sql('''SELECT * FROM df_table''').show(5) # Print the first 5 rows

#Plot the means group by variety
spark.sql('''SELECT MAX(sepal_length), variety FROM df_table GROUP BY variety''').show()
query=spark.sql('''SELECT MAX(sepal_length), variety FROM df_table GROUP BY variety''')

#Save the query output into a bucket
query.write.save(sys.argv[2] + '/Query_Iris_' + str(date), format="json")

#ML
#Pre-process the data
assembler = VectorAssembler(
    inputCols=['sepal_length', 'sepal_width','petal_length','petal_width'],
    outputCol="raw_features")
vector_df = assembler.transform(df)

# Scale features to have zero mean and unit standard deviation
standarizer = StandardScaler(withMean=True, withStd=True,
                              inputCol='raw_features',
                              outputCol='features')
model = standarizer.fit(vector_df)
vector_df = model.transform(vector_df)

# Convert label to number
indexer = StringIndexer(inputCol="variety", outputCol="label")
indexed = indexer.fit(vector_df).transform(vector_df)
indexed.show(10)

# Select features
iris = indexed.select(['features', 'label'])

# LR
train, test = iris.randomSplit([0.7, 0.3])
lr = LogisticRegression(labelCol="label", featuresCol="features", maxIter=10)
LRmodel = lr.fit(train)

# Print coefficients for our model
print("Coefficients: \n" + str(LRmodel.coefficientMatrix))
print("Intercept: " + str(LRmodel.interceptVector))

# Make predictions on the test dataset
with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    prediction = LRmodel.transform(test)
# Calculate accuracy
score = prediction.select(['label', 'prediction'])
acc = score.rdd.map(lambda x: x[0] == x[1]).sum() / float(score.count())
print('Accuracy: {}'.format(acc))

# Save the model on the output bucket
LRmodel.save(os.path.join(sys.argv[2] + '/Linear_Regression_Iris'))
import random
import sys 
import numpy as np
import pandas as pd
import quinn
import os

from pyspark.sql.types import IntegerType, DoubleType
from pyspark.sql.functions import col, desc
from pyspark.sql import SparkSession
from pyspark.context import SparkContext
from pyspark.ml.feature import VectorAssembler, Normalizer, StandardScaler
from pyspark.ml.classification import LogisticRegression, RandomForestClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder
from pyspark.ml import Pipeline, PipelineModel
from pyspark.ml.tuning import CrossValidatorModel

# Check for input arguments
if len(sys.argv) != 2:
    print("Usage: python predict.py <testFilePath>")
    sys.exit(1)


# Initialize Spark Session
sc = SparkContext('local')
spark = SparkSession(sc)

train_df = spark.read.format('csv').options(header='true', inferSchema='true', sep=';').load('/home/ubuntu/AWS_WinePrediction/TrainingDataset.csv')
valid_df = spark.read.format('csv').options(header='true', inferSchema='true', sep=';').load('/home/ubuntu/AWS_WinePrediction/ValidationDataset.csv')

# Load test dataset
test_file_path = sys.argv[1]
test_df = spark.read.format('csv').options(header='true', inferSchema='true', sep=';').load(test_file_path)
print("Data loaded into Spark.")
print(test_df.toPandas().head())

def remove_quotations(s):
    return s.replace('"', '')
  
train_df = quinn.with_columns_renamed(remove_quotations)(train_df)
train_df = train_df.withColumnRenamed('quality', 'label')

valid_df = quinn.with_columns_renamed(remove_quotations)(valid_df)
valid_df = valid_df.withColumnRenamed('quality', 'label')


test_df = quinn.with_columns_renamed(remove_quotations)(test_df)
test_df = test_df.withColumnRenamed('quality', 'label')

print("Data has been formatted.")
print(test_df.toPandas().head())

assembler = VectorAssembler(
    inputCols=["fixed acidity",
               "volatile acidity",
               "citric acid",
               "residual sugar",
               "chlorides",
               "free sulfur dioxide",
               "total sulfur dioxide",
               "density",
               "pH",
               "sulphates",
               "alcohol"],
                outputCol="inputFeatures")

scaler = Normalizer(inputCol="inputFeatures", outputCol="features")

## Only use LogisticRegression because this was the best model decided on
lr = LogisticRegression()
pipeline1 = Pipeline(stages=[assembler, scaler, lr])
paramgrid = ParamGridBuilder().build()
evaluator = MulticlassClassificationEvaluator(metricName="f1")
crossval = CrossValidator(estimator=pipeline1,  
                         estimatorParamMaps=paramgrid,
                         evaluator=evaluator, 
                         numFolds=3
                        )
cvModel1 = crossval.fit(train_df) 
print("F1 Score for Our Model: ", evaluator.evaluate(cvModel1.transform(valid_df)))

predictions = cvModel1.transform(test_df)
predictions.show()

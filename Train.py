import random
import sys 
import numpy as np
import pandas as pd
import quinn

from pyspark.sql.types import IntegerType, DoubleType
from pyspark.sql.functions import col, desc
from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler, Normalizer, StandardScaler
from pyspark.ml.classification import LogisticRegression, RandomForestClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder
from pyspark.ml import Pipeline

spark = SparkSession \
    .builder \
    .appName("CS643_Wine_Quality_Predictions_Project") \
    .master("spark://ip-172-31-26-28:7077") \
    .getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

## Load Training Dataset
train_df = spark.read.format('csv').options(header='true', inferSchema='true', sep=';').load('/home/ubuntu/AWS_WinePrediction/TrainingDataset.csv')
validation_df = spark.read.format('csv').options(header='true', inferSchema='true', sep=';').load('/home/ubuntu/AWS_WinePrediction/ValidationDataset.csv')

print("Data loaded from local directory on Master EC2 Instance.")
print(train_df.toPandas().head())

def remove_quotations(s):
    return s.replace('"', '')

train_df = quinn.with_columns_renamed(remove_quotations)(train_df)
train_df = train_df.withColumnRenamed('quality', 'label')

validation_df = quinn.with_columns_renamed(remove_quotations)(validation_df)
validation_df = validation_df.withColumnRenamed('quality', 'label')

print("Data has been formatted.")
print(train_df.toPandas().head())

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

lr = LogisticRegression()
rf = RandomForestClassifier()

pipeline1 = Pipeline(stages=[assembler, scaler, lr])
pipeline2 = Pipeline(stages=[assembler, scaler, rf])

paramgrid = ParamGridBuilder().build()

evaluator = MulticlassClassificationEvaluator(metricName="f1")

crossval = CrossValidator(estimator=pipeline1,  
                         estimatorParamMaps=paramgrid,
                         evaluator=evaluator, 
                         numFolds=3
                        )

cvModel1 = crossval.fit(train_df) 
f1_score_lr = evaluator.evaluate(cvModel1.transform(validation_df))
print("F1 Score for LogisticRegression Model: ", f1_score_lr)



crossval = CrossValidator(estimator=pipeline2,  
                         estimatorParamMaps=paramgrid,
                         evaluator=evaluator, 
                         numFolds=3
                        )

cvModel2 = crossval.fit(train_df) 
f1_score_rf = evaluator.evaluate(cvModel2.transform(validation_df))
print("F1 Score for RandomForestClassifier Model: ", f1_score_rf)

if f1_score_lr > f1_score_rf:
    print("Using Logistic Regression Model for predictions.")
else:
    print("Using Random Forest Model for predictions.")


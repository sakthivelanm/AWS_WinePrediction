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
from pyspark.ml import Pipeline, PipelineModel
from pyspark.ml.tuning import CrossValidatorModel

# Check for input arguments
if len(sys.argv) != 2:
    print("Usage: python predict.py <testFilePath>")
    sys.exit(1)


# Initialize Spark Session
spark = SparkSession \
    .builder \
    .appName("CS643_Wine_Quality_Predictions_Project") \
    .master("spark://ip-172-31-81-63:7077") \
    .getOrCreate()

# Load saved model
model_path = "/home/ubuntu/wineQualityLogisticModel/bestModel"
model = PipelineModel.load(model_path)

# Load test dataset
test_file_path = sys.argv[1]
test_df = spark.read.format('csv').options(header='true', inferSchema='true', sep=';').load(test_file_path)
print("Data loaded into Spark.")
print(test_df.toPandas().head())

def remove_quotations(s):
    return s.replace('"', '')
  
test_df = quinn.with_columns_renamed(remove_quotations)(test_df)
test_df = test_df.withColumnRenamed('quality', 'label')

print("Data has been formatted.")
print(test_df.toPandas().head())


# Make Predictions
predictions = model.transform(test_df)
predictions.select("features", "prediction").show()
# Save predictions to a CSV file
output_path = "/home/ubuntu/predictions.csv"
predictions.select("features", "prediction").write.csv(output_path, header=True)
print(f"Predictions saved to {output_path}")

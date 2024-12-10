FROM bitnami/spark:latest

USER root
RUN java -version
RUN apt-get update
RUN pip3 install pyspark pandas scikit-learn quinn

COPY . /app
WORKDIR /app

EXPOSE 4040

ENTRYPOINT ["python3", "Predict.py"]

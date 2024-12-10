FROM fokkodriesprong/docker-pyspark

USER root

WORKDIR /app
COPY . /app

RUN java -version
RUN pip3 install pyspark pandas quinn findspark

EXPOSE 4040

ENTRYPOINT ["python3", "DockerPredict.py"]

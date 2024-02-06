FROM python:3.11
USER root
RUN mkdir /mlops
COPY . /mlops
WORKDIR /mlops
RUN python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
ENV AIRFLOW_HOME=/mlops/airflow
ENV AIRFLOW__CORE__DAGBAG_IMPORT_TIMEOUT=1000
ENV AIRFLOW__CORE__ENABLE_XCOM_PICKLING=True
RUN airflow db init
RUN airflow users create -e rohanpatankar926@gmail.com -f rohan -l patankar -p admin -r Admin -u admin
RUN chmod 777 start.sh
RUN chmod 777 mlflow_run.sh
RUN apt update -y && apt install awscli -y
ENTRYPOINT [ "/bin/sh" ]
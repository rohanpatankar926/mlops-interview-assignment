FROM python:3.11
ENV AWS_ACCESS_KEY=""
ENV AWS_SECRET_KEY=""
ENV bucket_name=""
COPY . .
RUN pip install -r requirements.txt
CMD ["uvicorn","preds:app","--port","8000","--host","0.0.0.0"]
#FROM gcr.io/cloud-marketplace/google/python:latest
FROM marketplace.gcr.io/google/python:latest
RUN pip install flask
WORKDIR /myapp
COPY main.py /myapp/main.py
CMD ["python","main.py"]

FROM python:3.9-slim
RUN apt-get update && apt-get install curl -y
WORKDIR app
RUN mkdir file_content_monitor
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ./app/src .
ENTRYPOINT ["python", "main.py"]
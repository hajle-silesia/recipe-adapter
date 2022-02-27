FROM python:3.9-slim
WORKDIR app
RUN mkdir -p src/file_content_monitor
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ./app/src ./src
ENTRYPOINT ["python", "src/main.py"]
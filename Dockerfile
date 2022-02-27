FROM python:3.9-slim
WORKDIR app
RUN mkdir src
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ./app/src ./src
CMD ["python", "src/main.py"]
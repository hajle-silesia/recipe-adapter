FROM python:3.9-slim
RUN mkdir app
COPY ./app/src ./app
CMD ["python", "./app/main.py"]
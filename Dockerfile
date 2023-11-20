FROM python:3.11.6-slim
LABEL authors="sushka"

WORKDIR /usr/src/app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "main.py", "--config", "/config/config.json"]
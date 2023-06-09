FROM python:3.8

WORKDIR /app/data
WORKDIR /app

COPY requirements.txt .
RUN apt-get update
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt && rm requirements.txt

COPY . .

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--proxy-headers", "--log-config", "logging/logging.ini"]
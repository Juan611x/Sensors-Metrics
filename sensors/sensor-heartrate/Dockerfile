FROM python:3.11.9

WORKDIR /app

COPY heartrate_sensor.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "heartrate_sensor.py"]
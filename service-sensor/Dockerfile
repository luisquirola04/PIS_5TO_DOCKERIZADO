FROM python:3.12
ENV PYTHONUNBUFFERED 1
WORKDIR /api_sensor
COPY requirements.txt /api_sensor/
RUN pip install -r requirements.txt
COPY . /api_sensor/
CMD sleep 10 && python index.py

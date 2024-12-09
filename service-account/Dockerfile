FROM python:3.12
ENV PYTHONUNBUFFERED 1
WORKDIR /api_account
COPY requirements.txt /api_account/
RUN pip install -r requirements.txt
COPY . /api_account/
CMD sleep 10 && python index.py
    
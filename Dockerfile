FROM python:3.10

EXPOSE 8110

RUN mkdir -p /opt/services/bot/hw3_3
WORKDIR /opt/services/bot/hw3_3

COPY . /opt/services/bot/hw3_3

RUN pip install -r requirements.txt
CMD ["python", "/opt/services/bot/hw3_3/hw3_3.py"]
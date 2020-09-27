FROM python:3.8-slim

RUN pip install --upgrade pip

WORKDIR /opt/app/lib
COPY lib .
RUN pip install -r requirements.txt

WORKDIR /opt/app/services/client
COPY services/client .
RUN pip install -r requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/opt/app/"

CMD python __main__.py

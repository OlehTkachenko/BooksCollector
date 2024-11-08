FROM python:3

WORKDIR /bookscollector

RUN apt-get install libpq-dev

COPY ../requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY collector.py /bookscollector

ARG PSQL_URL
ARG SERVER_PORT

CMD [ "python", "-u", "/bookscollector/collector.py" ]

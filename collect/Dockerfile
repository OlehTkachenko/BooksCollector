FROM python:3

WORKDIR /bookscollector

RUN apt-get install libpq-dev

COPY requirements.txt /bookscollector

RUN pip install --no-cache-dir -r /bookscollector/requirements.txt

COPY collector.py /bookscollector

CMD [ "python", "-u", "/bookscollector/collector.py" ]
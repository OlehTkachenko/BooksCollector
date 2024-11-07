FROM python:3

WORKDIR /bookscollector

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY collector.py /bookscollector

CMD [ "python", "-u", "/bookscollector/collector.py" ]

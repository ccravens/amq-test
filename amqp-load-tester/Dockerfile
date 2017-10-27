FROM python:3.6-alpine

RUN apk update
RUN apk add g++ make

RUN pip install python-qpid-proton

COPY src/*.py /opt/app/
WORKDIR /opt/app

CMD python3 -u loadtester.py
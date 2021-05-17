FROM python:3.7-alpine

WORKDIR /api

RUN pip install flask
RUN pip install redis

COPY api/ .

EXPOSE 5000

CMD ["flask", "run"]

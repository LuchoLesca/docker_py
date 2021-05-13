FROM python:3.7-alpine

WORKDIR /api
COPY api/ .

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

RUN pip install flask
RUN pip install redis

EXPOSE 5000

CMD ["flask", "run"]

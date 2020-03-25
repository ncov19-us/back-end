From python:3.7

RUN apt-get update && apt-get install python3-pip -y

COPY . .

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
RUN set -ex && pip3 install -r requirements.txt

EXPOSE 8000
ENV PYTHONPATH /api

CMD uvicorn --host 0.0.0.0 --port 8000 --access-log api:APP --log-level info --reload
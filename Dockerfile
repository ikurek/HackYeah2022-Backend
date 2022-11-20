FROM python:3.9

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get install -y curl git wget unzip
RUN apt-get clean

COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip3 install torch==1.13.0 -f https://download.pytorch.org/whl/torch_stable.html
RUN pip3 install -r requirements.txt

COPY . /app

RUN python3 cold_run.py

EXPOSE 5000

ENV FLASK_APP=app.py

CMD ["flask", "run", "--host=0.0.0.0"]

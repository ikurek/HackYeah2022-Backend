FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get install -y curl git wget unzip python3 python3-distutils python3-pip
RUN apt-get clean

COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip3 install torch==1.13.0 -f https://download.pytorch.org/whl/torch_stable.html
RUN pip3 install -r requirements.txt

COPY . /app

EXPOSE 5000

RUN ["chmod", "+x", "/app/run_docker_server.sh"]

ENTRYPOINT [ "/app/run_docker_server.sh"]
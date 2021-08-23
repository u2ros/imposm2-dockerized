FROM python:2.7.16-jessie

RUN apt update && apt install -y libgdal1-dev libspatialindex-dev build-essential python-dev protobuf-compiler libprotobuf-dev libtokyocabinet-dev python-psycopg2 libgeos-c1

WORKDIR /app

#install python 2.7
#COPY install-python2.sh .
#RUN ./install-python2.sh

#install pip 2
RUN apt install -y wget
RUN wget https://bootstrap.pypa.io/pip/2.7/get-pip.py
RUN python2 get-pip.py --trusted-host pypi.org --trusted-host files.pythonhosted.org

#install pip and imposm

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install imposm

COPY . .

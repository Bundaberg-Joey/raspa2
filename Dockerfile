FROM continuumio/miniconda3

RUN apt-get -y update \
    && apt-get -y install

RUN conda install -c conda-forge raspa2

WORKDIR /app

FROM continuumio/miniconda3

RUN apt-get -y update \
    && apt-get -y install

RUN conda install -c conda-forge raspa2
RUN python3 -m pip install pandas numpy ase tqdm --no-cache-dir

WORKDIR /app

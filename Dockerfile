FROM nvcr.io/nvidia/cuda:11.6.2-cudnn8-runtime-ubuntu20.04 as base

RUN apt-get update && apt-get install -y wget

RUN wget --quiet \
  https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
  -O ~/miniconda.sh \
  && /bin/bash ~/miniconda.sh -b -p /opt/conda

RUN conda install -y -c conda-forge opencv

FROM base as main
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

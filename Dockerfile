FROM nvcr.io/nvidia/cuda:11.6.1-cudnn8-runtime-ubuntu20.04 as base

# install conda
RUN apt-get update && apt-get install -y wget
ENV CONDA_DIR /opt/conda
RUN wget --quiet \ 
    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \ 
    -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p $CONDA_DIR


ENV PATH=$CONDA_DIR/bin:$PATH

FROM base as main

# install opencv
RUN conda install -y -c conda-forge/label/gcc7 opencv

# CMD [ "python", "--version" ]
#COPY requirements.txt requirements.txt
#RUN pip install -r requirements.txt

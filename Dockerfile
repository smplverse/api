FROM nvcr.io/nvidia/cuda:11.6.1-cudnn8-runtime-ubuntu20.04 as base

# temporary fix for cuda cert rotation as of 30.04.2022
RUN apt-key del "7fa2af80" \
    && export this_distro="$(cat /etc/os-release | grep '^ID=' | awk -F'=' '{print $2}')" \
    && export this_version="$(cat /etc/os-release | grep '^VERSION_ID=' | awk -F'=' '{print $2}' | sed 's/[^0-9]*//g')" \
    && apt-key adv --fetch-keys "https://developer.download.nvidia.com/compute/cuda/repos/${this_distro}${this_version}/x86_64/3bf863cc.pub"


# install conda
RUN apt-get update && apt-get install -y \
    wget gcc ffmpeg libsm6 libxext6

ENV CONDA_DIR /opt/conda
RUN wget --quiet \
    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p $CONDA_DIR


ENV PATH=$CONDA_DIR/bin:$PATH

FROM base as main

# install opencv
RUN conda install -y -c conda-forge/label/gcc7 opencv

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

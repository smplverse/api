FROM ubuntu:20.04
WORKDIR /code
RUN apt-get update && apt-get install -y \
    python3-cytoolz \
    python3-dev \
    wget \
    gcc \
    ffmpeg \
    libsm6 \
    libxext6

ENV CONDA_DIR /opt/conda
RUN wget --quiet \
    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p $CONDA_DIR
ENV PATH=$CONDA_DIR/bin:$PATH
RUN conda install -y -c conda-forge opencv

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt --no-cache-dir
COPY . .
EXPOSE 80
CMD ["gunicorn", "src.app.app:app"]

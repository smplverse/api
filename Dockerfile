FROM nvidia/cuda:11.6.2-devel-ubi8 as base

FROM base as main
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

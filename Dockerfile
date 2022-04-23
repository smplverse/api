FROM piotrostr/smplverse as base

FROM base as main
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

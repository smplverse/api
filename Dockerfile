FROM jjanzic/docker-python3-opencv:4.1.0-opencv
WORKDIR /code
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt --no-cache-dir
COPY . .
EXPOSE 80
CMD ["gunicorn", "src.app.app:app"]

FROM python:3.10.15-bullseye

WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
  apt-get install -y \
  v4l-utils ffmpeg libsm6 libxext6

RUN pip3 install --upgrade pip
RUN pip3 install numpy==2.2.0 opencv-python==4.10.0.84

COPY run.py /app/run.py

CMD ["python3", "-u", "/app/run.py"]
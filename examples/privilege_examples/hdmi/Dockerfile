FROM python:3.10.15-bullseye
WORKDIR /app
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y \
    libx11-dev \
    x11-utils

RUN pip3 install --upgrade pip
RUN pip3 install python-xlib

COPY run.py /app/run.py
CMD ["python3", "-u", "/app/run.py"]

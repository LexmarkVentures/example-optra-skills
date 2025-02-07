FROM ubuntu:22.04

WORKDIR "/app"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update
RUN apt install -y libusb-1.0-0

RUN apt install -y vim
RUN apt install -y v4l-utils
RUN apt install -y python3-pip

COPY ./get-cam-settings.py /app/get-cam-settings.py

CMD ["python3", "-u", "/app/get-cam-settings.py"]
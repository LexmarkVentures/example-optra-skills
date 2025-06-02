FROM python:3.10.15-bullseye

WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive

RUN pip3 install --upgrade pip
RUN pip3 install asyncio azure-iot-device

COPY ./get-rtsp-async.py /app/get-rtsp-async.py
COPY ./get-rtsp.py /app/get-rtsp.py
COPY ./run_forever.py /app/run_forever.py

CMD ["python3", "-u", "/app/get-rtsp-async.py"]
# CMD ["python3", "-u", "/app/get-rtsp.py"]
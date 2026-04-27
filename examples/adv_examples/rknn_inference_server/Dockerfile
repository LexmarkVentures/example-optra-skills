# Stage 1: build the C++ inference server
FROM ubuntu:20.04 AS infer-build
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    cmake \
    build-essential \
    libmsgpack-dev

WORKDIR /inference-server
COPY inference_server/src src
COPY inference_server/CMakeLists.txt CMakeLists.txt
COPY inference_server/include include
COPY inference_server/lib /usr/local/lib
RUN mkdir build && cd build && cmake .. && make -j


# Stage 2: final Python runtime image
FROM python:3.10.15-bullseye

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    # OpenCV display dependencies
    libgl1 \
    libglib2.0-0 \
    x11-xserver-utils \
    v4l-utils \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip && \
    pip3 install \
        opencv-python \
        numpy \
        msgpack

WORKDIR /app

# Copy compiled inference server binary and its runtime library
COPY --from=infer-build /inference-server/inference-server /app/inference-server
COPY --from=infer-build /usr/local/lib/librknnrt.so /usr/local/lib/librknnrt.so
RUN ldconfig

# Copy the YOLOX-S RKNN model
COPY yolox_s.rknn /app/yolox_s.rknn

COPY run.py /app/run.py

CMD ["python3", "-u", "/app/run.py"]

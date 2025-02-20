FROM nvcr.io/nvidia/l4t-pytorch:r35.2.1-pth2.0-py3

WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive

COPY run.py /app/run.py

RUN python3 -c "import torchvision; model = torchvision.models.detection.fasterrcnn_resnet50_fpn(weights=torchvision.models.detection.FasterRCNN_ResNet50_FPN_Weights.DEFAULT)"

CMD ["python3", "-u", "/app/run.py"]

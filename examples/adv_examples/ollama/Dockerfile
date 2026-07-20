FROM nvcr.io/nvidia/l4t-jetpack:r36.4.0

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    python3-pip \
    zstd && \
    rm -rf /var/lib/apt/lists/*

ARG OLLAMA_VERSION=0.30.0
ARG OLLAMA_INSTALL_DIR=/usr/local

RUN curl -fsSLO "https://github.com/ollama/ollama/releases/download/v${OLLAMA_VERSION}/ollama-linux-arm64.tar.zst" && \
    tar -xf ollama-linux-arm64.tar.zst -C "${OLLAMA_INSTALL_DIR}" && \
    rm ollama-linux-arm64.tar.zst && \
    curl -fsSLO "https://github.com/ollama/ollama/releases/download/v${OLLAMA_VERSION}/ollama-linux-arm64-jetpack6.tar.zst" && \
    tar -xf ollama-linux-arm64-jetpack6.tar.zst -C "${OLLAMA_INSTALL_DIR}" && \
    rm ollama-linux-arm64-jetpack6.tar.zst

WORKDIR /app

RUN pip3 install --no-cache-dir azure-iot-device

COPY download_models.py entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

ENV OLLAMA_HOST=0.0.0.0
ENV OLLAMA_MODELS=/app/storage/ollama

EXPOSE 11434

ENTRYPOINT ["/app/entrypoint.sh"]

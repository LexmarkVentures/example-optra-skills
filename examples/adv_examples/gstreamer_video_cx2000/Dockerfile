FROM ubuntu:noble-20260113

# Install required packages.
# Clean up in the same RUN command to reduce the image size.
RUN apt-get update && apt-get install -y \
    alsa-base \
    openssh-server \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Additional setup for SSH
RUN mkdir /var/run/sshd
RUN sed -i 's/^#Port 22/Port 2200/' /etc/ssh/sshd_config
EXPOSE 2200

# Copy video early for improved rebuilds when modifying source.
COPY video /video

# Configure authorized_keys for SSH access
RUN mkdir -p /root/.ssh && chmod 700 /root/.ssh
COPY authorized_keys /root/.ssh/authorized_keys
RUN chmod 600 /root/.ssh/authorized_keys

COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

COPY app /app
WORKDIR /app

CMD ["/app/app.sh"]

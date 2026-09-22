FROM debian:bookworm-slim@sha256:3783cc01769c7b2b1b83a5c5ad96c815348e28ed7da68e2e3687004faa906251
RUN apt-get update && apt-get install -y --no-install-recommends python3 libpython3.11 python3-venv python3-tk binutils procps xvfb xauth ca-certificates && rm -rf /var/lib/apt/lists/*
RUN python3 -m venv /opt/build-env && /opt/build-env/bin/pip install --no-cache-dir pyinstaller==6.22.3
ENV PATH="/opt/build-env/bin:${PATH}"
WORKDIR /work

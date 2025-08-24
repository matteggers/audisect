# Dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    # docker complains if I don't make a new user
    PIP_ROOT_USER_ACTION=ignore

ENV XDG_CACHE_HOME=/cache \
    HF_HOME=/cache/hf \
    NLTK_DATA=/cache/nltk

ENV HF_HUB_DISABLE_TELEMETRY=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src

# Choose CUDA channel to match driver (cu121 | cu124 | cu126 | cu128)
ARG TORCH_CHANNEL=cu128
RUN python -m pip install -U pip && \
    python -m pip install --no-cache-dir --index-url https://download.pytorch.org/whl/${TORCH_CHANNEL} "torch>=2.6"

RUN python -m pip install --no-cache-dir .

ENTRYPOINT ["audisect"]
CMD ["--help"]
# space constraint
FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    libsndfile1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# throw everything into app dir
COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt


ENTRYPOINT ["python", "audisect.py"]

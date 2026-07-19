FROM python:3.13-slim

WORKDIR /app

# Clean up dependencies
RUN apt-get update && apt-get install -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir --upgrade pip setuptools wheel

# HARD-CODED INLINE PIP: This completely bypasses the corrupt requirements.txt file cache block
RUN pip3 install --no-cache-dir --only-binary=:all: "numpy>=2.1.0" "pandas>=2.2.0" "scipy>=1.14.0" "requests>=2.32.0"

COPY . /app

ENV PYTHONUNBUFFERED=1

CMD ["python3", "main.py"]

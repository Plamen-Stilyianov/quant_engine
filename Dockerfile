FROM python:3.13-slim

WORKDIR /app

# Clean up dependencies
RUN apt-get update && apt-get install -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir --upgrade pip setuptools wheel

# Copy requirements context to compile or gather pre-built platform wheels
COPY requirements.txt .

# Compile and package everything into an isolated wheel directory
# (Leverages native binaries for arm64/amd64 when available to prevent long builds)
RUN pip3 wheel --no-cache-dir --wheel-dir /build/wheels -r requirements.txt

COPY . /app

ENV PYTHONUNBUFFERED=1

CMD ["python3", "main.py"]

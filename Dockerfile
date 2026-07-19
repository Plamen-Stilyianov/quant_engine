FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Optimize python layer builds by caching requirements maps
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /app

# Ensure logging outputs push instantly to the PyCharm interface console panel
ENV PYTHONUNBUFFERED=1

CMD ["python3", "main.py"]

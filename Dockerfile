FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    wget \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install chromium
RUN playwright install-deps

COPY . .

# Stellen Sie sicher, dass 8000 der Standardport ist, 
# aber erlauben Sie, dass er durch die PORT-Umgebungsvariable überschrieben wird
ENV PORT=8000
EXPOSE $PORT

# Verwenden Sie python direkt für die main.py, die jetzt die PORT-Umgebungsvariable liest
CMD ["python", "main.py"]
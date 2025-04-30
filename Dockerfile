FROM python:3.12-slim

# Install system deps
RUN apt-get update && apt-get install -y \
    curl unzip wget gnupg libnss3 libgconf-2-4 libxss1 libappindicator3-1 libasound2 libatk-bridge2.0-0 libcups2 \
    libgtk-3-0 xdg-utils fonts-liberation && rm -rf /var/lib/apt/lists/*

# Install Chrome
RUN curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google.list && \
    apt-get update && apt-get install -y google-chrome-stable

# Install Python deps
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy app
COPY . /app
WORKDIR /app

CMD ["python3", "extractor.py"]

# 1. Choose a base image
FROM python:3.12-slim

# 2. Set working directory inside the container
WORKDIR /app

# 3. Copy dependency list
COPY requirements.txt .

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy application code
COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

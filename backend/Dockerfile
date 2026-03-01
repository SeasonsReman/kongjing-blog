FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Explicitly create SQLite database at build time if it doesn't exist to ensure permissions
RUN python -c "import sqlite3; sqlite3.connect('blog.db').close()"

EXPOSE 8000

# Start command using dynamic port provided by cloud host (Render/Zeabur)
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]

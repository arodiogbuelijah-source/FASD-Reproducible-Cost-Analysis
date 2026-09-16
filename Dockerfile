FROM python:3.12.14-slim
WORKDIR /app
COPY . /app
ENV PYTHONPATH=/app/src PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
CMD ["python", "scripts/benchmark.py", "--runs", "30"]

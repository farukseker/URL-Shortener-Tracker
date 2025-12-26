FROM python:3.14-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN pip install uv && uv pip install --system --no-cache

COPY req .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

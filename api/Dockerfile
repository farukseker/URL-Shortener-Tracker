FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh

ENV PATH="/root/.local/bin:$PATH"

COPY pyproject.toml uv.lock ./
COPY requirements/base.txt base.txt
RUN uv add -r base.txt
RUN uv sync --frozen --no-install-project
RUN uv add uvicorn

# venv binaries
ENV PATH="/app/.venv/bin:$PATH"

COPY . .

#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

ENTRYPOINT ["uv", "run", "uvicorn", "main:app", "--host" , "0.0.0.0", "--port", "8080"]

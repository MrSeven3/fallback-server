FROM python:3.14-slim

WORKDIR /usr/src/fallback-server

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

COPY . .

CMD ["uv", "run", "uwsgi", "--http", "0.0.0.0:8000", "--wsgi-file", "app.py", "--callable", "app", "--buffer-size", "32768"]
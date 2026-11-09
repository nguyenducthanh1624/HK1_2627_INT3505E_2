# ─── stage 1: builder ───
FROM python:3.12-slim AS builder
WORKDIR /build
COPY pyproject.toml ./
COPY src ./src
RUN pip install --no-cache-dir uv \
 && uv venv /opt/venv
ENV VIRTUAL_ENV=/opt/venv \
 PATH=/opt/venv/bin:$PATH
RUN uv pip install --no-cache .
# src đã được copy ở bước trên
# package đã được cài trong venv
# ─── stage 2: runtime ───
FROM python:3.12-slim
WORKDIR /app
RUN groupadd -r app && \
 useradd -r -g app -d /app app
# Copy venv từ builder

COPY --from=builder --chown=app:app /opt/venv /opt/venv
COPY --chown=app:app wsgi.py ./wsgi.py
COPY --chown=app:app gunicorn.conf.py ./gunicorn.conf.py
# Source nằm trong package đã cài
ENV VIRTUAL_ENV=/opt/venv \
 PATH=/opt/venv/bin:$PATH \
 PYTHONUNBUFFERED=1
USER app
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "product_api.factory:create_app()"]
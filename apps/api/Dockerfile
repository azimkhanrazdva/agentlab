FROM python:3.12-slim

WORKDIR /app
COPY pyproject.toml ./
COPY apps ./apps
COPY packages ./packages
COPY tests ./tests
RUN pip install --no-cache-dir -e ".[dev]"
EXPOSE 8000
CMD ["uvicorn", "agentlab_api.main:app", "--host", "0.0.0.0", "--port", "8000"]


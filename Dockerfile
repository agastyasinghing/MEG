FROM python:3.11-slim

WORKDIR /app

# Copy dependency manifests first for layer caching
COPY requirements.txt pyproject.toml ./

RUN pip install --no-cache-dir -r requirements.txt

# Copy the package and runtime config
COPY meg/ ./meg/
COPY config/ ./config/

# Install meg as an editable package so `python -m meg.*` works
RUN pip install --no-cache-dir -e .

# Default: run the bot. Docker Compose overrides this per service.
CMD ["python", "-m", "meg.main"]

FROM python:3.11-slim

WORKDIR /app

# Copy dependency manifests first for layer caching
COPY requirements.txt pyproject.toml ./

RUN pip install --no-cache-dir -r requirements.txt

# Copy the package and runtime config
COPY meg/ ./meg/
COPY config/ ./config/

# setuptools is needed for editable installs in slim images; install it explicitly
# then install meg as an editable package so `python -m meg.*` resolves correctly
RUN pip install --no-cache-dir setuptools
RUN pip install --no-cache-dir -e .

# Verify the entry point is importable at build time
RUN python -c "import meg.main"

# Report unhealthy if the main process (PID 1) has exited
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import os; os.kill(1, 0)"

# Default: run the bot. Docker Compose overrides this per service.
CMD ["python", "-m", "meg.main"]

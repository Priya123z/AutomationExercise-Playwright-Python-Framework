FROM python:3.12-slim

# Runs as a non-root user with the same uid the CI runner uses, so artifacts written to
# the mounted volume are owned by the host and do not need chown afterwards.
RUN useradd --create-home --uid 1000 runner

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN playwright install-deps chromium

# WORKDIR created /app as root; the test user needs to write .pytest_cache here.
RUN chown runner:runner /app

USER runner

RUN playwright install chromium

COPY --chown=runner:runner . .

CMD ["pytest", "-n", "2", "-q"]

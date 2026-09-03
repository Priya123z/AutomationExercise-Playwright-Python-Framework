FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Browsers go somewhere world readable rather than into one user's home, so the
# container can run as whatever uid the host passes with --user and still find them.
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

RUN playwright install --with-deps chromium \
    && chmod -R a+rX /ms-playwright

COPY . .

# An arbitrary --user has no home and cannot write to /app, so keep pytest's scratch
# files out of both.
ENV HOME=/tmp

CMD ["pytest", "-n", "2", "-q", "-p", "no:cacheprovider"]

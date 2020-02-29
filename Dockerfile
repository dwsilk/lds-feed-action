FROM python:3.7-slim AS builder
ADD . /app
WORKDIR /app

RUN python -m pip install --upgrade pip
RUN pip install --target=/app atoma beautifulsoup4 pendulum requests

# A distroless container image with Python and some basics like SSL certificates
# https://github.com/GoogleContainerTools/distroless
FROM gcr.io/distroless/python3-debian10
COPY --from=builder /app /app
WORKDIR /app
ENV PYTHONPATH /app
CMD ["/app/main.py"]

# temp stage
FROM python:3.11.4-slim-buster as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y --no-install-recommends gcc

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt


# final stage
FROM python:3.11.4-slim-buster

WORKDIR /app
COPY ./src/ /app

COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

RUN pip install --no-cache /wheels/*

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
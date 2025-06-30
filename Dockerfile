#stage 1: Build dependencies

FROM python:3.10-slim AS build
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

#Stage 2: Final image

FROM python:3.10-slim
RUN useradd -m python
WORKDIR /home/python/app
COPY --from=builder /root/.local /home/appuser/.local
ENV PATH=/home/appuser/.local/bin:$PATH
COPY --chown=python:python . .
USER python
EXPOSE 5000
CMD ["python", "main.py"]

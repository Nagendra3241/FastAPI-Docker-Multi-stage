#stage 1: Build dependencies

FROM python:3.12-slim AS build
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

#Stage 2: Final image

FROM python:3.12-slim
RUN useradd -m python
WORKDIR /home/python/app
COPY --from=builder /root/.local /home/python/.local
ENV PATH=/home/python/.local/bin:$PATH
COPY --chown=python:python . .
USER python
EXPOSE 5000
CMD ["python", "main.py"]

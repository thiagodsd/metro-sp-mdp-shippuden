FROM rust:1.75-slim AS rust-builder

RUN apt-get update && apt-get install -y \
    python3-dev \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir --break-system-packages maturin

WORKDIR /build
COPY packages/metro-mdp-lib ./packages/metro-mdp-lib

WORKDIR /build/packages/metro-mdp-lib
RUN maturin build --release

FROM python:3.11-slim

WORKDIR /app

COPY --from=rust-builder /build/packages/metro-mdp-lib/target/wheels/*.whl /tmp/
RUN pip install --no-cache-dir --break-system-packages /tmp/*.whl && rm /tmp/*.whl

COPY backend/requirements.txt .
RUN pip install --no-cache-dir --break-system-packages -r requirements.txt

COPY backend/app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

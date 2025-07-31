# syntax=docker/dockerfile:experimental

FROM --platform=$BUILDPLATFORM python:3.13-slim AS builder

ARG TARGETPLATFORM
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    gfortran \
    git \
    libatlas-base-dev \
    libavcodec-dev \
    libavformat-dev \
    libgtk-3-dev \
    libjpeg-dev \
    libpng-dev \
    libswscale-dev \
    libx11-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

# Install dlib from source (static)
# RUN git clone -b 'v20.0' --single-branch https://github.com/davisking/dlib.git && \
#     cd dlib && \
#     python3 setup.py install --set BUILD_SHARED_LIBS=OFF --no USE_AVX_INSTRUCTIONS

# Create venv and install other packages
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

RUN pip install --upgrade pip && \
    pip install aiohttp face_recognition fastapi python-multipart setuptools==80.9.0 uvicorn

# Final image
FROM python:3.13-slim AS final

COPY --from=builder /venv /venv
ENV PATH="/venv/bin:$PATH"

WORKDIR /app
COPY facerec.py index.html /app/

EXPOSE 8000
CMD ["uvicorn", "facerec:app", "--host", "0.0.0.0", "--port", "8000"]

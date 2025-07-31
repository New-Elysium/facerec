# 🧠 Face Comparison API

A simple FastAPI app to compare two faces using the [`face_recognition`](https://github.com/ageitgey/face_recognition) library.  
Supports both:
- Uploading two image files
- Providing two image URLs

Built with Python 3.13, `face_recognition`, and multi-arch Docker support (runs on ARM64 and x86_64).

---

## 🚀 Features

- ✅ Compare faces from uploaded images
- ✅ Compare faces from image URLs
- ✅ Dockerized with multi-arch support (Raspberry Pi 4 & cloud)
- ✅ Uses `aiohttp` for efficient async downloads
- ✅ Powered by `dlib` and deep learning-based 128D face embeddings

---

## 🐳 Docker Build & Run

### 1. Build Multi-Arch Image

```bash
docker buildx create --name multiarch-builder --use
docker buildx build --platform linux/amd64,linux/arm64 \
  -t yourdockerhubuser/face-compare:latest \
  --push .

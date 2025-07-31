#!/bin/bash

TARGET=$1

case "$TARGET" in
  "linux/amd64")
    ARCH_DIR="x86_64-linux-gnu"
    ;;
  "linux/arm64")
    ARCH_DIR="aarch64-linux-gnu"
    ;;
  "linux/arm/v7")
    ARCH_DIR="arm-linux-gnueabihf"
    ;;
  *)
    echo "Unsupported TARGETPLATFORM: $TARGET"
    exit 1
    ;;
esac

mkdir -p /shared-libs/lib /shared-libs/usr/lib

cp /lib/$ARCH_DIR/*.so.* /shared-libs/lib/ || true
cp /usr/lib/$ARCH_DIR/libX11.so.6 /shared-libs/usr/lib/ || true
# Add more as needed

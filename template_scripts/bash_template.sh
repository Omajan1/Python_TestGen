#!/usr/bin/env bash
set -e

NAME="--NAME--"

# Paths
IMG_PATH="./${NAME}.img"
MNT_DIR="/mnt/fs"

# NORMAL OPERATION

# 100 MB test image.
dd if=/dev/zero of="$IMG_PATH" bs=1M count=--SIZE--

# create filesystem inside image file.
# <start mkfs>

# <end mkfs>

# Mount point inside output_images
mkdir -p "$MNT_DIR"

# Mount the filesystem using a loop device
sudo mount -o loop "$IMG_PATH" "$MNT_DIR"

# <start ops>

# <end ops>

# Clean Up
sudo umount "$MNT_DIR"

# Done
echo ">> Image created"
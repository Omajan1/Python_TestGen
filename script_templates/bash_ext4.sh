#!/bin/bash
set -e

SCRIPT_DIR=$(pwd)
OUTPUT_DIR="."
NAME="ext4-test"

IMG_PATH="${OUTPUT_DIR}/${NAME}.img"
MNT_DIR="/mnt/${NAME}_mnt"

# 10 MB test image.
dd if=/dev/zero of="$IMG_PATH" bs=1M count=10

# create filesystem inside image file.
mkfs.ext4 -O ^has_journal -E lazy_itable_init=0,lazy_journal_init=0 "$IMG_PATH"

# Mount point inside output_images
mkdir -p "$MNT_DIR"

# Mount the filesystem using a loop device
sudo mount -o loop "$IMG_PATH" "$MNT_DIR"

# Space for normal filesystem calls/operations.
cd "$MNT_DIR"
mkdir -p testtxts
cd testtxts
echo "helloworld" > testfile.txt

# Manipulate the ext4 structures directly in the image file using debugfs


# CLEAN UP - Unmount after operations are done
sudo umount "$MNT_DIR"

echo ">> Image created"
exit 0
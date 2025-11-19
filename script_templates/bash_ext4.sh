#!/bin/bash
set -e

SCRIPT_DIR=$(pwd)
OUTPUT_DIR="."
NAME="ext4-test"

IMG_PATH="${OUTPUT_DIR}/${NAME}.img"
MNT_DIR="/mnt/${NAME}_mnt"

# -------------------------
# CLEAN OPTION
# -------------------------
if [[ "$1" == "--clean" ]]; then
    echo ">> Unmounting and cleaning image..."

    # Unmount if mounted
    if mountpoint -q "$MNT_DIR"; then
        sudo umount "$MNT_DIR"
        echo ">> Unmounted $MNT_DIR"
    else
        echo ">> $MNT_DIR is not mounted"
    fi

    # Delete image
    if [[ -f "$IMG_PATH" ]]; then
        rm "$IMG_PATH"
        echo ">> Deleted $IMG_PATH"
    else
        echo ">> No image file found to delete"
    fi

    exit 0
fi

# -------------------------
# NORMAL OPERATION
# -------------------------

# 10 MB test image.
dd if=/dev/zero of="$IMG_PATH" bs=1M count=10

# create filesystem inside image file.
mkfs.ext4 -O ^has_journal -E lazy_itable_init=0,lazy_journal_init=0 "$IMG_PATH"

# Mount point inside output_images
mkdir -p "$MNT_DIR"

# Mount the filesystem using a loop device
sudo mount -o loop "$IMG_PATH" "$MNT_DIR"

# Optional: give your user ownership so you don't need sudo for every file op
# sudo chown -R "$USER:$USER" "$MNT_DIR"

# Space for normal filesystem calls/operations.
cd "$MNT_DIR"
mkdir -p testtxts
cd testtxts
echo "helloworld" > testfile.txt

# Manipulate the ext4 structures directly in the image file using debugfs

# Done
echo ">> Image created, mounted, and test file written."
echo ">> To clean: ./bash_ext4.sh --clean"

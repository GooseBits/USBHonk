#!/usr/bin/env bash
set -e

# Run from the directory of the script
cd $( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

##
## Configuration
##
RPI_ZIP_URL="https://downloads.raspberrypi.org/raspios_lite_armhf/images/raspios_lite_armhf-2021-05-28/2021-05-07-raspios-buster-armhf-lite.zip"
RPI_ZIP_HASH="c5dad159a2775c687e9281b1a0e586f7471690ae28f2f2282c90e7d59f64273c"
RPI_ZIP=$(basename $RPI_ZIP_URL)
RPI_IMAGE="${RPI_ZIP/.zip/.img}"
OUTPUT_FILE="usbhonk.img"
MOUNT_PATH="/tmp/usbhonk_rootfs"
TEMP_IMAGE_SIZE="8G" # Just needs to be big enough for initial image, final image will be truncated

if [ $EUID != 0 ]; then
    echo "Please run as root"
    exit 1
fi

DEPENDENCIES=( kpartx qemu-arm-static unzip mkfs.ext4 resize2fs e2fsck tune2fs xz wget zerofree truncate sfdisk )

HAS_DEPS=1
for i in "${DEPENDENCIES[@]}"
do
    if ! command -v $i &> /dev/null
    then
        echo "You are missing $i, make sure it's installed."
        HAS_DEPS=0
    fi
done

if [[ $HAS_DEPS != 1 ]]; then
    exit 1
fi

if [ ! -f "./$RPI_IMAGE" ]
then
    if [ ! -f "$RPI_ZIP" ]
    then
        echo "Downloading Raspberry Pi OS Image..."
        wget -q "$RPI_ZIP_URL"
    fi
    if ! tmp=$(sha256sum ./$RPI_ZIP | grep $RPI_ZIP_HASH);
    then
        echo "$RPI_ZIP looks corrupt, delete it and rerun the script."
        exit 1
    fi
    echo "Extracting Raspberry Pi OS Image..."
    unzip -q "./$RPI_ZIP"
fi

## Copy the image to the target
cp -f "$RPI_IMAGE" "$OUTPUT_FILE"

## Resize the target image
truncate -s "$TEMP_IMAGE_SIZE" "$OUTPUT_FILE"

## Grow the rootfs partition to the max
echo ", +" | sfdisk -q -N2 "$OUTPUT_FILE"

## Attach the image
KPARTX_OUTPUT=$(kpartx -av "$OUTPUT_FILE")

DEVICE=/dev/$(echo "$KPARTX_OUTPUT"|grep -Po loop[0-9]|head -n 1)
BOOT_PARTITION=/dev/mapper/$(echo "$KPARTX_OUTPUT"|grep -Po loop[0-9]+p1)
ROOT_PARTITION=/dev/mapper/$(echo "$KPARTX_OUTPUT"|grep -Po loop[0-9]+p2)

## Resize root partition filesystem
e2fsck -f $ROOT_PARTITION
resize2fs $ROOT_PARTITION > /dev/null
tune2fs -m0 $ROOT_PARTITION > /dev/null

## Mount filesystem
mkdir -p $MOUNT_PATH
mount $ROOT_PARTITION $MOUNT_PATH
mount $BOOT_PARTITION $MOUNT_PATH/boot

## Add our setup scripts into the target
cp -r chroot_installer $MOUNT_PATH/tmp/

## Copy qemu-arm-static into the target
cp $(which qemu-arm-static) $MOUNT_PATH/tmp/chroot_installer/

## Enter the ARM chroot and run the installation
chroot $MOUNT_PATH /tmp/chroot_installer/qemu-arm-static /bin/bash /tmp/chroot_installer/init.sh

## Remove install files
echo "Cleaning up installation files..."
rm -rf $MOUNT_PATH/tmp/chroot_installer

## Umount filesystem
echo "Unmounting filesystems..."
umount $MOUNT_PATH/boot
umount $MOUNT_PATH
rmdir $MOUNT_PATH

## Shrink the root filesystem to the minimum size
e2fsck -f "$ROOT_PARTITION"
resize2fs -M "$ROOT_PARTITION" > /dev/null
ROOTFS_INFO=$(tune2fs -l "$ROOT_PARTITION")
BLOCK_SIZE=$(echo "$ROOTFS_INFO" |grep "^Block size"|grep -Po "[0-9]+")
BLOCK_COUNT=$(echo "$ROOTFS_INFO" |grep "^Block count"|grep -Po "[0-9]+")
SECTOR_SIZE="512"
ROOTFS_SIZE=$((BLOCK_COUNT * BLOCK_SIZE))
ROOTFS_SECTORS=$((ROOTFS_SIZE / SECTOR_SIZE))

## Shrink the rootfs partition to the minimum
echo ", $ROOTFS_SECTORS" | sfdisk -q -N2 "$OUTPUT_FILE"

## Run ZeroFree so the image compresses better
echo "Zeroing free space..."
zerofree "$ROOT_PARTITION"
sync

## Remove mappings
echo "Cleaning up mappings..."
kpartx -d "$OUTPUT_FILE"

## Truncate the image
echo "Truncating image..."
SFDISK_OUTPUT=$(sfdisk -J "$OUTPUT_FILE")
ROOTFS_START=$(echo "$SFDISK_OUTPUT" | jq .partitiontable.partitions[1].start)
IMAGE_SIZE=$(((ROOTFS_START + ROOTFS_SECTORS) * SECTOR_SIZE))
truncate -s "$IMAGE_SIZE" "$OUTPUT_FILE"

# Compress the image for release
#echo "Compressing image for release..."
#xz -f -k -T0 --arm -9 "$OUTPUT_FILE"

echo "Success! HONK!"

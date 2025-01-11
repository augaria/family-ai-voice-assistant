#!/bin/bash

# Detect the package manager
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
else
    echo "Cannot detect the operating system."
    exit 1
fi

# Update and install packages based on the detected OS
case $OS in
    ubuntu|debian)
        sudo apt-get update
        sudo apt-get install -y --no-install-recommends \
            build-essential \
            g++ \
            sox \
            alsa-utils \
            portaudio19-dev \
            libatlas-base-dev \
            linux-headers-generic
        ;;
    centos|rhel)
        sudo yum update
        sudo yum install -y \
            @development \
            gcc-c++ \
            sox \
            alsa-utils \
            portaudio-devel \
            atlas-devel \
            kernel-headers \
            alsa-lib
        ;;
    fedora)
        sudo dnf update
        sudo dnf install -y \
            @development-tools \
            gcc-c++ \
            sox \
            alsa-utils \
            portaudio-devel \
            atlas-devel \
            kernel-headers \
            alsa-lib
        ;;
    arch)
        sudo pacman -Syu
        sudo pacman -S --noconfirm \
            base-devel \
            gcc \
            sox \
            alsa-utils \
            portaudio \
            lapack \
            linux-headers \
            alsa-lib
        ;;
    *)
        echo "Unsupported OS: $OS"
        exit 1
        ;;
esac

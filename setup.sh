#!/bin/bash

# W8IPCameraHK Auto Setup Script
# Supports Termux (Android) and Linux

echo "[+] Starting setup..."

# Detect Termux
if [ -n "$PREFIX" ] && [ -x "$(command -v pkg)" ]; then
    echo "[+] Detected Termux. Installing dependencies with pkg..."
    pkg update -y
    pkg install -y python clang
else
    echo "[+] Assuming Linux. Installing dependencies with apt..."
    sudo apt update
    sudo apt install -y python3 python3-pip
fi

# Ensure pip is available as 'pip'
if ! command -v pip &> /dev/null; then
    if command -v pip3 &> /dev/null; then
        alias pip=pip3
    fi
fi

# Install Python requirements
if [ -f requirements.txt ]; then
    echo "[+] Installing Python dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
else
    echo "[!] requirements.txt not found!"
    exit 1
fi

echo "[+] Setup complete! You can now run the tool with:"
echo "    python W8CameraHack.py" 

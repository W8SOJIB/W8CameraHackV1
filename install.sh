#!/bin/bash

# Installation script for Bangladesh Camera Scanner
# Supports both Termux and Linux

echo "╔═══════════════════════════════════════╗"
echo "║  Bangladesh Camera Scanner Installer  ║"
echo "║        Credit: W8Team/W8SOJIB         ║"
echo "╚═══════════════════════════════════════╝"
echo ""
echo "[*] Developed by: W8Team/W8SOJIB"
echo "[*] Termux Compatible"
echo ""

# Detect environment
if [ -d "$PREFIX" ] && [ -n "$ANDROID_ROOT" ]; then
    echo "[*] Termux environment detected"
    ENV="termux"
else
    echo "[*] Linux/Unix environment detected"
    ENV="linux"
fi

# Update package manager
if [ "$ENV" = "termux" ]; then
    echo "[*] Updating Termux packages..."
    pkg update -y
    pkg upgrade -y
    
    echo "[*] Installing Python..."
    pkg install python -y
else
    echo "[*] Checking Python installation..."
    if ! command -v python3 &> /dev/null; then
        echo "[!] Python3 not found. Please install Python3 first."
        exit 1
    fi
fi

# Install Python dependencies
echo "[*] Installing Python packages..."
pip install --upgrade pip

echo "[*] Installing required packages..."
pip install requests aiohttp pyfiglet

echo "[*] Installing optional packages..."
pip install colorama

# Check if installation was successful
if [ $? -eq 0 ]; then
    echo ""
    echo "╔═══════════════════════════════════════╗"
    echo "║   Installation Complete! ✓            ║"
    echo "╚═══════════════════════════════════════╝"
    echo ""
    echo "Run the scanner with:"
    echo "  python camera_scanner.py"
    echo ""
else
    echo "[!] Some packages failed to install, but the script may still work."
    echo "[*] Try running: python camera_scanner.py"
fi


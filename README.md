# W8IPCameraHK - Camera Scanner

[GitHub Repository](https://github.com/W8SOJIB/W8CameraHack)

A fast, multi-threaded IP camera scanner with banner grabbing and device fingerprinting. Supports Windows, Linux, and Termux (Android).

## Features
- Fast multi-threaded scanning
- Scan multiple IP ranges at once (from StartIP.txt and EndIP.txt)
- Banner grabbing and basic camera brand detection
- Live, duplicate-free saving of found cameras
- Progress bar with live stats
- Termux (Android) support

## Requirements
- Python 3.7+
- pip (Python package manager)

## Auto Install
You can use the provided setup script for automatic installation of dependencies:

```sh
bash setup.sh
```

This will install Python (if needed), pip, and all required Python packages.

## Manual Installation

### 1. Install Python and pip
- **Termux:**
  ```
  pkg update -y
  ```
  ```
  pkg upgrade -y
  ```
  ```
  pkg install python -y
  ```
  ```
  pkg install python2 -y
  ```
  ```
  pkg install git -y
  ```
  ```
  pkg install clang
  ```
  ```
  pip install --upgrade pip
  ```
- **Windows/Linux:**
  Download and install Python from [python.org](https://www.python.org/downloads/).

### 2. Download the script

```
git clone https://github.com/W8SOJIB/W8CameraHack
```

```
cd W8CameraHack
```

```
ls
```

### 3. Install dependencies
```sh
pip install -r requirements.txt
```
```
python W8CameraHack.py
```

## Usage

Donload IP-LIST
https://onlytoolsbd.com/IP-List/

### 1. Prepare IP Range Files
- Create `StartIP.txt` and `EndIP.txt` in the same directory.
- Each line in `StartIP.txt` should have a start IP, and the corresponding line in `EndIP.txt` should have the end IP for that range.
- Example:
  - StartIP.txt:
    ```
    192.168.1.1
    10.0.0.1
    ```
  - EndIP.txt:
    ```
    192.168.1.255
    10.0.0.255
    ```

### 2. Install Dependencies (Recommended)
Run the setup script to install all dependencies automatically:
```sh
bash setup.sh
```

### 3. Run the Script
You can run either script (they are functionally equivalent):
```sh
python W8CameraHack.py

```
- On Termux, you may need to use:
  ```sh
  python W8CameraHack.py
  ```

### 4. Set Max Threads
- When prompted, enter the number of threads (e.g., 300 for fast scan, or lower for low-power devices).

### 5. Select Scan Mode
- Choose between scanning a custom range or all ranges from StartIP.txt/EndIP.txt.

### 6. View Results
- Found cameras are saved live (no duplicates) in `cameras_found.txt`.
- Each entry includes the camera URL and, if detected, the brand.

## Termux Tips
- Use a reasonable thread count (e.g., 50-150) for best performance on mobile devices.
- You can edit text files with `vim`, `nano`, or `micro` in Termux.
- If you see permission errors, try running `termux-setup-storage`.

## Exit
- Press `Ctrl+C` or select Exit in the menu. The script will thank you for using it.

## Credits
Made By @W8SOJIB 

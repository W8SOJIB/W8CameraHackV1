# Scan Controls Guide

## 🎮 Keyboard Controls

### During Active Scanning

| Key Combination | Action | Description |
|----------------|--------|-------------|
| **Ctrl+C** | ⛔ **STOP** | Immediately stops the scan and exits |
| **Ctrl+Z** | ⏸️ **PAUSE/RESUME** | Toggles pause state (Linux/Mac/Termux only) |

## 🔍 How It Works

### Ctrl+C (Stop Immediately)
- Sends `SIGINT` signal
- Sets global `stop_scan = True` flag
- All worker threads check this flag
- Threads exit gracefully
- Program terminates with `sys.exit(0)`
- **No delay** - instant shutdown!

### Ctrl+Z (Pause/Resume)
- Sends `SIGTSTP` signal (Unix/Linux/Mac/Termux)
- Toggles `pause_scan` flag
- When paused:
  - All worker threads enter wait state
  - No new scans are performed
  - Display: `[⏸] SCAN PAUSED`
- Press again to resume:
  - Workers continue from where they stopped
  - Display: `[▶] SCAN RESUMED`

## 💡 Features

### Thread Safety
- Global flags are checked in all worker threads
- Timeout on queue operations (0.5 seconds)
- Graceful shutdown with 1-second cleanup period

### Live Feedback
```
[⏸] SCAN PAUSED - Press Ctrl+Z again to resume...
[▶] SCAN RESUMED - Continuing...
[!] Ctrl+C detected - STOPPING IMMEDIATELY...
```

### Platform Support
- **Ctrl+C**: ✅ All platforms (Windows, Linux, Mac, Termux)
- **Ctrl+Z**: ✅ Linux, Mac, Termux | ❌ Windows (not supported)

## 📱 Termux Specific

On Termux (Android):
- Both Ctrl+C and Ctrl+Z work perfectly
- Use volume-down + C for Ctrl+C
- Use volume-down + Z for Ctrl+Z
- Instant response on both controls

## 🚀 Quick Examples

### Stop Scanning
1. Press `Ctrl+C`
2. See: `[!] Ctrl+C detected - STOPPING IMMEDIATELY...`
3. Program exits immediately

### Pause and Resume
1. Press `Ctrl+Z` during scan
2. See: `[⏸] SCAN PAUSED - Press Ctrl+Z again to resume...`
3. Check results in `CCTV Found.txt`
4. Press `Ctrl+Z` again
5. See: `[▶] SCAN RESUMED - Continuing...`
6. Scan continues from where it paused

## ⚡ Performance

- **Stop Time**: < 1 second
- **Pause Response**: Instant (next thread cycle)
- **Resume Response**: Instant
- **No Data Loss**: All found cameras are saved before stopping

---

**Developed by:** W8Team/W8SOJIB  
**GitHub:** [github.com/W8SOJIB](https://github.com/W8SOJIB)


# SysInfo CLI

System information monitor for Linux servers - beautiful CLI tool.

## Features

- 🖥️ **System Info** - OS, kernel, CPU, memory, disk, network
- 📊 **Realtime Monitor** - Live CPU, memory, network usage
- 🔧 **Process Manager** - View and manage processes
- 🎨 **Beautiful Interface** - ANSI colors, ASCII art, progress bars
- 🐧 **All Linux Distros** - Ubuntu, Debian, Fedora, Arch, and more

## Installation

### One-click install (recommended)

```bash
curl -fsSL https://raw.githubusercontent.com/wudixiaozhao111/sysinfo-cli/main/install.sh | bash
```

### Via pip

```bash
pip3 install sysinfo-cli
```

## Usage

```bash
# Interactive mode (default)
sysinfo-cli

# Direct views
sysinfo-cli -s    # System info
sysinfo-cli -m    # Realtime monitor
sysinfo-cli -p    # Process manager
```

## Screenshots

### System Info
![System Info](https://raw.githubusercontent.com/wudixiaozhao111/sysinfo-cli/main/screenshots/screenshot-1-system-en.png)

### Realtime Monitor
![Realtime Monitor](https://raw.githubusercontent.com/wudixiaozhao111/sysinfo-cli/main/screenshots/screenshot-2-monitor-en.png)

### Process Manager
![Process Manager](https://raw.githubusercontent.com/wudixiaozhao111/sysinfo-cli/main/screenshots/screenshot-3-processes-en.png)

## Requirements

- Python 3.6+
- psutil >= 5.0.0

## License

MIT License

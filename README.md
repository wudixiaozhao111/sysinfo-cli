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

### Supported Distributions

| Distribution Family | Examples | Installation Method |
|---------------------|----------|---------------------|
| Debian/Ubuntu | Ubuntu, Debian, Linux Mint, Pop!_OS, elementary OS | deb package |
| Red Hat/Fedora | Fedora, CentOS, RHEL, Rocky Linux, AlmaLinux | dnf + script |
| Arch Linux | Arch, Manjaro, EndeavourOS, Garuda | pacman + script |
| openSUSE | openSUSE Leap, openSUSE Tumbleweed | zypper + script |
| Gentoo | Gentoo, Funtoo | emerge + script |
| Alpine | Alpine Linux | apk + script |
| Slackware | Slackware, Slackware-based | pkgtool + script |
| Void Linux | Void Linux | xbps + script |
| Solus | Solus | eopkg + script |
| NixOS | NixOS | nix-env + script |
| **Any other Linux** | All others | Universal script |

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

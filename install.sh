#!/bin/bash
# SysInfo CLI - One-click Install Script
# Supports: All Linux distributions
# - Debian/Ubuntu family: deb package
# - Red Hat/Fedora family: dnf + script
# - Arch Linux family: pacman + script
# - openSUSE: zypper + script
# - Gentoo: emerge + script
# - Alpine: apk + script
# - Slackware: pkgtool + script
# - Void Linux: xbps + script
# - Solus: eopkg + script
# - NixOS: nix-env + script
# - All others: universal script

set -e

echo "=============================================="
echo "  SysInfo CLI - System Information Monitor"
echo "  Server Edition v1.0.0"
echo "=============================================="
echo ""

# GitHub repo
GITHUB_REPO="wudixiaozhao111/sysinfo-cli"
GITHUB_RAW="https://raw.githubusercontent.com/$GITHUB_REPO/main"
GITHUB_RELEASE="https://github.com/$GITHUB_REPO/releases/download/v1.0.0"

# Check if running as root
check_root() {
    if [ "$EUID" -ne 0 ]; then
        SUDO="sudo"
    else
        SUDO=""
    fi
}

# Detect Linux distribution
detect_distro() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        DISTRO=$ID
        DISTRO_NAME=$PRETTY_NAME
        DISTRO_LIKE=$ID_LIKE
    elif [ -f /etc/redhat-release ]; then
        DISTRO="rhel"
        DISTRO_NAME=$(cat /etc/redhat-release)
        DISTRO_LIKE="rhel fedora"
    elif [ -f /etc/arch-release ]; then
        DISTRO="arch"
        DISTRO_NAME="Arch Linux"
        DISTRO_LIKE="arch"
    elif [ -f /etc/alpine-release ]; then
        DISTRO="alpine"
        DISTRO_NAME="Alpine Linux"
        DISTRO_LIKE="alpine"
    elif [ -f /etc/gentoo-release ]; then
        DISTRO="gentoo"
        DISTRO_NAME="Gentoo Linux"
        DISTRO_LIKE="gentoo"
    elif [ -f /etc/slackware-version ]; then
        DISTRO="slackware"
        DISTRO_NAME=$(cat /etc/slackware-version)
        DISTRO_LIKE="slackware"
    elif [ -f /etc/void-release ]; then
        DISTRO="void"
        DISTRO_NAME="Void Linux"
        DISTRO_LIKE="void"
    else
        DISTRO="unknown"
        DISTRO_NAME="Unknown Linux"
        DISTRO_LIKE=""
    fi
    echo "Detected: $DISTRO_NAME"
    echo ""
}

# Check if distro is in a family
is_distro_family() {
    local family=$1
    # Check direct match
    if [ "$DISTRO" = "$family" ]; then
        return 0
    fi
    # Check ID_LIKE
    for id in $DISTRO_LIKE; do
        if [ "$id" = "$family" ]; then
            return 0
        fi
    done
    return 1
}

# Universal install method (download script directly)
install_via_script() {
    local pkg_manager=$1
    local python_pkg=$2
    local psutil_pkg=$3
    
    echo "Installing via universal script method..."
    echo ""
    
    # Install dependencies
    echo "Installing dependencies (python3 + psutil)..."
    
    case $pkg_manager in
        apt)
            $SUDO apt-get update
            $SUDO apt-get install -y "$python_pkg" "$psutil_pkg"
            ;;
        dnf)
            $SUDO dnf install -y "$python_pkg" "$psutil_pkg"
            ;;
        yum)
            $SUDO yum install -y "$python_pkg" "$psutil_pkg"
            ;;
        pacman)
            $SUDO pacman -Sy --noconfirm "$python_pkg" "$psutil_pkg"
            ;;
        zypper)
            $SUDO zypper --non-interactive install "$python_pkg" "$psutil_pkg"
            ;;
        apk)
            $SUDO apk add --no-cache "$python_pkg" "$psutil_pkg"
            ;;
        emerge)
            $SUDO emerge --ask=n "$python_pkg" "$psutil_pkg"
            ;;
        xbps)
            $SUDO xbps-install -y "$python_pkg" "$psutil_pkg"
            ;;
        eopkg)
            $SUDO eopkg install -y "$python_pkg" "$psutil_pkg"
            ;;
        nix)
            nix-env -iA nixpkgs.python3 nixpkgs.python3Packages.psutil
            ;;
        *)
            echo "Please install python3 and python3-psutil manually first."
            echo "Then run this script again."
            exit 1
            ;;
    esac
    
    echo ""
    echo "Downloading sysinfo-cli..."
    
    # Download the script
    TMP_SCRIPT=$(mktemp /tmp/sysinfo-cli.XXXXXX.py)
    curl -sL -o "$TMP_SCRIPT" "$GITHUB_RAW/sysinfo_cli.py"
    
    # Install to /usr/local/bin
    echo "Installing to /usr/local/bin/sysinfo-cli..."
    $SUDO install -m 755 "$TMP_SCRIPT" /usr/local/bin/sysinfo-cli
    
    rm -f "$TMP_SCRIPT"
    
    echo ""
    echo "✓ Installation complete!"
    echo "Run: sysinfo-cli"
}

# Install via deb (Debian/Ubuntu)
install_via_deb() {
    echo "Installing via deb package..."
    echo ""
    
    # Download deb package
    TMP_DEB=$(mktemp /tmp/sysinfo-cli.XXXXXX.deb)
    echo "Downloading sysinfo-cli..."
    curl -sL -o "$TMP_DEB" "$GITHUB_RELEASE/sysinfo-cli_1.0.0-1_all.deb"
    
    # Install dependencies
    echo "Installing dependencies..."
    $SUDO apt-get update
    $SUDO apt-get install -y python3 python3-psutil
    
    # Install deb package
    echo "Installing sysinfo-cli..."
    $SUDO dpkg -i "$TMP_DEB" || $SUDO apt-get install -f -y
    
    rm -f "$TMP_DEB"
    
    echo ""
    echo "✓ Installation complete!"
    echo "Run: sysinfo-cli"
}

# Main
check_root
detect_distro

# Choose installation method based on distro
if is_distro_family "debian" || is_distro_family "ubuntu"; then
    echo "Distribution: Debian/Ubuntu family"
    echo ""
    echo "Installation methods:"
    echo "  1. deb package (recommended)"
    echo "  2. Universal script"
    echo ""
    read -p "Choose method [1/2] (default 1): " choice
    choice=${choice:-1}
    
    if [ "$choice" = "1" ]; then
        install_via_deb
    else
        install_via_script apt python3 python3-psutil
    fi

elif is_distro_family "fedora" || is_distro_family "rhel" || is_distro_family "centos"; then
    echo "Distribution: Red Hat/Fedora family"
    echo ""
    echo "Installing via dnf + script..."
    echo ""
    
    # Check if dnf or yum
    if command -v dnf &> /dev/null; then
        install_via_script dnf python3 python3-psutil
    else
        install_via_script yum python3 python3-psutil
    fi

elif is_distro_family "arch"; then
    echo "Distribution: Arch Linux family"
    echo ""
    echo "Installing via pacman + script..."
    echo ""
    install_via_script pacman python python-psutil

elif is_distro_family "opensuse" || is_distro_family "suse"; then
    echo "Distribution: openSUSE family"
    echo ""
    echo "Installing via zypper + script..."
    echo ""
    install_via_script zypper python3 python3-psutil

elif is_distro_family "alpine"; then
    echo "Distribution: Alpine Linux"
    echo ""
    echo "Installing via apk + script..."
    echo ""
    install_via_script apk python3 py3-psutil

elif is_distro_family "gentoo"; then
    echo "Distribution: Gentoo Linux"
    echo ""
    echo "Installing via emerge + script..."
    echo ""
    install_via_script emerge dev-lang/python dev-python/psutil

elif is_distro_family "void"; then
    echo "Distribution: Void Linux"
    echo ""
    echo "Installing via xbps + script..."
    echo ""
    install_via_script xbps python3 python3-psutil

elif [ "$DISTRO" = "solus" ]; then
    echo "Distribution: Solus"
    echo ""
    echo "Installing via eopkg + script..."
    echo ""
    install_via_script eopkg python3 python3-psutil

elif [ "$DISTRO" = "nixos" ] || command -v nix-env &> /dev/null; then
    echo "Distribution: NixOS"
    echo ""
    echo "Installing via nix-env + script..."
    echo ""
    install_via_script nix python3 python3-psutil

elif [ "$DISTRO" = "slackware" ]; then
    echo "Distribution: Slackware"
    echo ""
    echo "Slackware detected. Please install python3 and psutil manually,"
    echo "then download sysinfo_cli.py from GitHub and run it directly."
    echo ""
    echo "Download: $GITHUB_RAW/sysinfo_cli.py"
    exit 1

else
    echo "Distribution: $DISTRO_NAME"
    echo ""
    echo "Unknown distribution, using universal installation method."
    echo ""
    
    # Try to detect package manager
    if command -v apt-get &> /dev/null; then
        install_via_script apt python3 python3-psutil
    elif command -v dnf &> /dev/null; then
        install_via_script dnf python3 python3-psutil
    elif command -v yum &> /dev/null; then
        install_via_script yum python3 python3-psutil
    elif command -v pacman &> /dev/null; then
        install_via_script pacman python python-psutil
    elif command -v zypper &> /dev/null; then
        install_via_script zypper python3 python3-psutil
    elif command -v apk &> /dev/null; then
        install_via_script apk python3 py3-psutil
    else
        echo "Could not detect package manager."
        echo ""
        echo "Please install python3 and psutil manually, then download:"
        echo "  $GITHUB_RAW/sysinfo_cli.py"
        echo ""
        echo "And run it with: python3 sysinfo_cli.py"
        exit 1
    fi
fi

echo ""
echo "=============================================="
echo "  Thanks for using SysInfo CLI!"
echo "  https://github.com/$GITHUB_REPO"
echo "=============================================="

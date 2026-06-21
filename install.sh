#!/bin/bash
# SysInfo CLI - One-click Install Script
# Supports: Ubuntu/Debian, Fedora/CentOS/RHEL, Arch/Manjaro, openSUSE, and more

set -e

echo "=============================================="
echo "  SysInfo CLI - System Information Monitor"
echo "  Server Edition v1.0.0"
echo "=============================================="
echo ""

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
    elif [ -f /etc/redhat-release ]; then
        DISTRO="rhel"
        DISTRO_NAME=$(cat /etc/redhat-release)
    elif [ -f /etc/arch-release ]; then
        DISTRO="arch"
        DISTRO_NAME="Arch Linux"
    else
        DISTRO="unknown"
        DISTRO_NAME="Unknown"
    fi
    echo "Detected: $DISTRO_NAME"
    echo ""
}

# Install via pip (universal method)
install_via_pip() {
    echo "Installing via pip..."
    
    # Check if pip is available
    if ! command -v pip3 &> /dev/null; then
        echo "pip3 not found, installing python3-pip..."
        case $DISTRO in
            ubuntu|debian|linuxmint|pop|elementary)
                $SUDO apt-get update
                $SUDO apt-get install -y python3-pip python3-psutil
                ;;
            fedora|rhel|centos|rocky|almalinux)
                $SUDO dnf install -y python3-pip python3-psutil
                ;;
            arch|manjaro|endeavouros)
                $SUDO pacman -Sy --noconfirm python-pip python-psutil
                ;;
            opensuse*|suse)
                $SUDO zypper install -y python3-pip python3-psutil
                ;;
            *)
                echo "Please install python3-pip and python3-psutil manually first."
                exit 1
                ;;
        esac
    fi
    
    # Install sysinfo-cli
    echo "Installing sysinfo-cli..."
    $SUDO pip3 install sysinfo-cli
    
    echo ""
    echo "✓ Installation complete!"
    echo "Run: sysinfo-cli"
}

# Install via deb (Debian/Ubuntu)
install_via_deb() {
    echo "Installing via deb package..."
    
    # Download deb package
    TMP_DEB=$(mktemp /tmp/sysinfo-cli.XXXXXX.deb)
    echo "Downloading sysinfo-cli..."
    curl -sL -o "$TMP_DEB" "https://github.com/wudixiaozhao111/sysinfo-cli/releases/download/v1.0.0/sysinfo-cli_1.0.0-1_all.deb"
    
    # Install dependencies
    $SUDO apt-get update
    $SUDO apt-get install -y python3 python3-psutil
    
    # Install deb package
    $SUDO dpkg -i "$TMP_DEB" || $SUDO apt-get install -f -y
    
    rm -f "$TMP_DEB"
    
    echo ""
    echo "✓ Installation complete!"
    echo "Run: sysinfo-cli"
}

# Install via AUR (Arch Linux)
install_via_aur() {
    echo "Installing from AUR..."
    
    # Check if yay or paru is available
    if command -v yay &> /dev/null; then
        AUR_HELPER="yay"
    elif command -v paru &> /dev/null; then
        AUR_HELPER="paru"
    else
        echo "No AUR helper found (yay/paru). Installing via git..."
        
        # Install base-devel if needed
        if ! command -v makepkg &> /dev/null; then
            $SUDO pacman -Sy --noconfirm base-devel
        fi
        
        # Clone and build
        TMP_DIR=$(mktemp -d /tmp/sysinfo-cli-aur.XXXXXX)
        cd "$TMP_DIR"
        git clone https://aur.archlinux.org/sysinfo-cli.git
        cd sysinfo-cli
        makepkg -si --noconfirm
        
        cd /
        rm -rf "$TMP_DIR"
        
        echo ""
        echo "✓ Installation complete!"
        echo "Run: sysinfo-cli"
        return
    fi
    
    $AUR_HELPER -S --noconfirm sysinfo-cli
    
    echo ""
    echo "✓ Installation complete!"
    echo "Run: sysinfo-cli"
}

# Install via dnf (Fedora/CentOS/RHEL)
install_via_dnf() {
    echo "Installing via COPR..."
    
    # Check if COPR repo is available, otherwise use pip
    if command -v dnf &> /dev/null; then
        # Try COPR first
        if $SUDO dnf copr enable -y sysinfo/sysinfo-cli 2>/dev/null; then
            $SUDO dnf install -y sysinfo-cli
            echo ""
            echo "✓ Installation complete!"
            echo "Run: sysinfo-cli"
            return
        fi
    fi
    
    # Fallback to pip
    echo "COPR not available, falling back to pip..."
    install_via_pip
}

# Main
check_root
detect_distro

# Choose installation method based on distro
case $DISTRO in
    ubuntu|debian|linuxmint|pop|elementary)
        echo "Distribution: Debian/Ubuntu family"
        echo ""
        echo "Installation methods:"
        echo "  1. deb package (recommended)"
        echo "  2. pip (universal)"
        echo ""
        read -p "Choose method [1/2] (default 1): " choice
        choice=${choice:-1}
        
        if [ "$choice" = "1" ]; then
            install_via_deb
        else
            install_via_pip
        fi
        ;;
    
    fedora|rhel|centos|rocky|almalinux)
        echo "Distribution: Red Hat/Fedora family"
        echo ""
        echo "Installation methods:"
        echo "  1. COPR (recommended)"
        echo "  2. pip (universal)"
        echo ""
        read -p "Choose method [1/2] (default 1): " choice
        choice=${choice:-1}
        
        if [ "$choice" = "1" ]; then
            install_via_dnf
        else
            install_via_pip
        fi
        ;;
    
    arch|manjaro|endeavouros)
        echo "Distribution: Arch Linux family"
        echo ""
        echo "Installation methods:"
        echo "  1. AUR (recommended)"
        echo "  2. pip (universal)"
        echo ""
        read -p "Choose method [1/2] (default 1): " choice
        choice=${choice:-1}
        
        if [ "$choice" = "1" ]; then
            install_via_aur
        else
            install_via_pip
        fi
        ;;
    
    opensuse*|suse)
        echo "Distribution: openSUSE family"
        echo ""
        echo "Installing via pip..."
        install_via_pip
        ;;
    
    *)
        echo "Distribution: $DISTRO_NAME"
        echo ""
        echo "Using universal pip installation..."
        install_via_pip
        ;;
esac

echo ""
echo "=============================================="
echo "  Thanks for using SysInfo CLI!"
echo "  https://github.com/wudixiaozhao111/sysinfo-cli"
echo "=============================================="

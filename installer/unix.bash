#!/usr/bin/env bash

set -e

echo "🔍 Detecting operating system..."

OS="$(uname -s)"

case "$OS" in
    Linux*)   OS_TYPE="linux" ;;
    Darwin*)  OS_TYPE="macos" ;;
    *)        echo "❌ Unsupported OS: $OS"; exit 1 ;;
esac

echo "✅ OS detected: $OS_TYPE"


# ============================================================
# Install Python & Dependencies
# ============================================================

install_linux_dependencies() {
    echo "📦 Installing dependencies for Linux..."

    if command -v apt >/dev/null 2>&1; then
        sudo apt update
        sudo apt install -y python3 python3-pip python3-venv git curl
    elif command -v dnf >/dev/null 2>&1; then
        sudo dnf install -y python3 python3-pip python3-virtualenv git curl
    elif command -v yum >/dev/null 2>&1; then
        sudo yum install -y python3 python3-pip python3-virtualenv git curl
    elif command -v pacman >/dev/null 2>&1; then
        sudo pacman -Sy --noconfirm python python-pip git curl
    else
        echo "❌ Unsupported Linux distribution"
        exit 1
    fi
}

install_macos_dependencies() {
    echo "📦 Installing dependencies for macOS..."

    if ! command -v brew >/dev/null 2>&1; then
        echo "🍺 Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi

    brew install python git
}


# ============================================================
# Install SnortAMV CLI
# ============================================================

install_tool() {
    echo "⬇ Downloading SnortAMV..."

    INSTALL_DIR="$HOME/.snortamv"
    mkdir -p "$INSTALL_DIR"

    # Download CLI (you must replace this URL)
    curl -fsSL https://yourdomain.com/snortamv.py -o "$INSTALL_DIR/snortamv.py"

    chmod +x "$INSTALL_DIR/snortamv.py"


    # Add symlink to PATH
    echo "🔗 Creating symlink..."

    if [ -d "/usr/local/bin" ] && [ "$(id -u)" = "0" ]; then
        ln -sf "$INSTALL_DIR/snortamv.py" /usr/local/bin/snortamv
    else
        mkdir -p "$HOME/.local/bin"
        ln -sf "$INSTALL_DIR/snortamv.py" "$HOME/.local/bin/snortamv"

        # Ensure ~/.local/bin is in PATH
        if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
            echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
            echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.zshrc"
        fi
    fi

    echo "🎉 SnortAMV installed!"
}


# ============================================================
# Verify installation
# ============================================================

verify_install() {
    echo "🔎 Verifying installation..."

    if command -v snortamv >/dev/null 2>&1; then
        echo "✅ SnortAMV is ready!"
    else
        echo "⚠ Installed but PATH not updated — restart terminal."
    fi
}


# ============================================================
# Main Execution
# ============================================================

if [ "$OS_TYPE" = "linux" ]; then
    install_linux_dependencies
else
    install_macos_dependencies
fi

install_tool
verify_install

#!/data/data/com.termux/files/usr/bin/bash
# FloX Tools - Auto Installer

clear
echo "╔══════════════════════════════════════════╗"
echo "║      🔥 FWX Tools - Installer 🔥          ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# Cek Termux
if [ ! -d "/data/data/com.termux" ]; then
    echo "[!] Script ini buat Termux Android!"
    exit 1
fi

# Update packages
echo "[*] Update Termux packages..."
pkg update -y > /dev/null 2>&1
pkg upgrade -y > /dev/null 2>&1

# Install dependencies
echo "[*] Install Node.js, Python, Git..."
pkg install -y nodejs python git > /dev/null 2>&1

# Install Python packages
echo "[*] Install Python packages..."
pip install -r requirements.txt > /dev/null 2>&1

# Install Node packages
echo "[*] Install Node packages..."
npm install > /dev/null 2>&1

# Buat folder
mkdir -p ddos

# Permission
chmod +x run.sh push.sh obfuscate.sh encrypt.sh 2>/dev/null

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║         ✅ INSTALL SUKSES! ✅            ║"
echo "╚══════════════════════════════════════════╝"
echo ""
echo "🚀 Cara jalanin:"
echo "   bash run.sh"
echo ""

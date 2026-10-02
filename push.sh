#!/data/data/com.termux/files/usr/bin/bash
# Auto Push ke GitHub

echo "╔══════════════════════════════════════════╗"
echo "║       🔥 FWX Tools - Auto Push 🔥         ║"
echo "╚══════════════════════════════════════════╝"
echo ""

if ! command -v git > /dev/null 2>&1; then
    echo "[!] Git belum install. Jalankan: bash install.sh"
    exit 1
fi

if ! git config user.name > /dev/null 2>&1; then
    echo "[!] Git belum di-config."
    echo "   git config --global user.name \"NamaLu\""
    echo "   git config --global user.email \"email@lu.com\""
    exit 1
fi

echo "[*] Encrypting tools.py..."
bash encrypt.sh
echo ""

echo "[*] Obfuscating api.js..."
bash obfuscate.sh
echo ""

echo "[*] Git add..."
git add .

echo ""
read -p "[?] Commit message (enter buat default): " MSG
MSG=${MSG:-"Update $(date +%Y-%m-%d_%H:%M)"}

git commit -m "$MSG"

echo ""
echo "[*] Push ke GitHub..."
git push

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║         ✅ PUSH SUKSES! ✅               ║"
echo "╚══════════════════════════════════════════╝"

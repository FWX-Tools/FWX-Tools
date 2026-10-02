#!/data/data/com.termux/files/usr/bin/bash
# FloX Tools - Auto Run API + Tools

clear
echo "╔══════════════════════════════════════════╗"
echo "║       🔥 FWX Tools - Booting 🔥           ║"
echo "╚══════════════════════════════════════════╝"
echo ""

if [ ! -f "tools.py" ]; then
    echo "[!] tools.py gak ditemukan!"
    exit 1
fi

if [ ! -f "api.js" ]; then
    echo "[!] api.js gak ditemukan!"
    exit 1
fi

if ! command -v node > /dev/null 2>&1; then
    echo "[!] Node.js belum install. Jalankan: bash install.sh"
    exit 1
fi

if ! command -v python > /dev/null 2>&1; then
    echo "[!] Python belum install. Jalankan: bash install.sh"
    exit 1
fi

# Start API di background
echo "[*] Starting License API..."
node api.js > api.log 2>&1 &
API_PID=$!
echo "[✓] API running (PID: $API_PID)"

sleep 3

if curl -s http://127.0.0.1:2009/ > /dev/null 2>&1; then
    echo "[✓] API connected"
else
    echo "[!] API belum siap, lanjut..."
fi

echo ""
echo "[*] Starting Tools..."
echo ""

trap "echo ''; echo '[*] Stopping API...'; kill $API_PID 2>/dev/null; exit" INT TERM

python tools.py

echo ""
echo "[*] Stopping API..."
kill $API_PID 2>/dev/null
echo "[✓] Selesai"

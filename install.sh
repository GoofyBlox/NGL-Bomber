echo "[+] Installing NGL Spam Bomber..."
pkg update && pkg upgrade -y
pkg install python -y
pip install requests
echo "[+] Done! Run: python main.py"

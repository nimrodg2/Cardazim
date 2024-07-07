echo "[SERVER] Installing dependencies…"
pip install flask
pip install PyCryptodome
pip install Pillow
echo "[SERVER] Done installing dependencies."
echo "[SERVER] Running Server"
python ./server.py 127.0.0.1 5000 "\Testing"
echo "Server Down"
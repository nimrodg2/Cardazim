echo "[CLIENT] Installing dependencies…"
pip install PyCryptodome
pip install Pillow
echo "Done installing dependencies."
echo "[CLIENT] Launching client..."
python ./client.py 127.0.0.1 5000 "Iran" "Nimrod" "Testing\Iran_Pigeon.png" "Where is Raisi?" "down"
echo "[CLIENT] sent message"
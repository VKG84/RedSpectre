#!/bin/bash

echo "[+] Installation de RedSpectre..."

sudo mkdir -p /opt/redspectre
sudo cp -r * /opt/redspectre

echo "[+] Installation des dépendances (Kali compatible)..."
pip3 install --break-system-packages -r /opt/redspectre/requirements.txt

sudo cp /opt/redspectre/icon.png /usr/share/pixmaps/redspectre.png

echo "[Desktop Entry]
Name=RedSpectre
Exec=python3 /opt/redspectre/main.py
Icon=redspectre
Terminal=false
Type=Application
Categories=Utility;Security;" | sudo tee /usr/share/applications/redspectre.desktop > /dev/null

chmod +x /opt/redspectre/main.py
echo "[+] RedSpectre installé. Lancez-le depuis le menu ou via : python3 /opt/redspectre/main.py"

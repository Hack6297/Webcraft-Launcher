#!/bin/bash
mkdir -p ~/.local/share/applications

cat <<EOF > ~/.local/share/applications/webcraft.desktop
[Desktop Entry]
Name=WebCraft
Exec=python3 ~/Downloads/webcraft_client.py --nickname=%u
Type=Application
NoDisplay=true
MimeType=x-scheme-handler/webcraft;
EOF

xdg-mime default webcraft.desktop x-scheme-handler/webcraft
chmod +x ~/.local/share/applications/webcraft.desktop

echo "✅ WebCraft launcher registered!"

#!/bin/bash
echo "Building executable with PyInstaller..."
source venv/bin/activate
pyinstaller --noconfirm --onedir --windowed --add-data "Amiri.ttf:." --name "MissionTrack_DZ" ui_main.py
echo "Build complete. Check the 'dist/MissionTrack_DZ' directory."

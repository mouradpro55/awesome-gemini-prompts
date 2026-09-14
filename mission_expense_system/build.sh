#!/bin/bash
# Script to build the executable using PyInstaller
echo "Building executable with PyInstaller..."
source venv/bin/activate
pyinstaller --noconfirm --onedir --windowed --name "MissionExpenseSystem" main.py
echo "Build complete. Check the 'dist/MissionExpenseSystem' directory."

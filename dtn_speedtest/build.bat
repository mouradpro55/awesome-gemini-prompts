@echo off
echo Building DTN Speedtest Windows Executable...
echo Make sure you are in a Python virtual environment and have run "pip install -r requirements.txt"
pyinstaller --noconfirm --onedir --windowed --name "DTN_Speedtest" --add-data "core.py;." "main.py"
echo Build Complete! Check the "dist" folder.
pause
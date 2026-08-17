@echo off
echo Installing required packages...
python -m pip install -r requirements.txt
echo Building DTN Speedtest Windows Executable...
python -m PyInstaller --noconfirm --onedir --windowed --name "DTN_Speedtest" --add-data "core.py;." "main.py"
echo Build Complete! Check the "dist" folder.
pause
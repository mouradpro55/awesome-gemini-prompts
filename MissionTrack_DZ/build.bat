@echo off
echo Preparing environment for MissionTrack_DZ...

IF NOT EXIST "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install -r requirements.txt

echo Building executable with PyInstaller for Windows...
python -m PyInstaller --noconfirm --onedir --windowed --version-file=version_info.txt --add-data "Amiri.ttf;." --add-data "Template.xlsx;." --add-data "templates;templates" --hidden-import "webview" --hidden-import "docx" --name "MissionTrack_DZ" main.py

echo Build complete. Check the "dist\MissionTrack_DZ" directory.
pause

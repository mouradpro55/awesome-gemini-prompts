@echo off
echo Building Bootable USB Creator for Windows...
echo.

REM Activate virtual environment if it exists, otherwise just try to use global pyinstaller
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

REM Install PyInstaller if not present
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

REM Ensure dependencies are installed
echo Checking dependencies...
pip install -r requirements.txt

REM Build the executable
echo Compiling...
pyinstaller --noconfirm --onedir --windowed --add-data "venv/Lib/site-packages/customtkinter;customtkinter/" --name "Bootable_USB_Creator" "main.py"

echo.
echo Build complete! Check the 'dist' folder.
pause

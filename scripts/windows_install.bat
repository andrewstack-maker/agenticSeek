@echo off
echo Starting installation for Windows...

REM Install Python dependencies from requirements.txt
pip install -r requirements.txt

REM Install Selenium
pip install selenium

echo Note: pyAudio installation may require additional steps on Windows.
echo Please install portaudio manually (e.g., via vcpkg or prebuilt binaries) and then run: pip install pyaudio
echo Also, download and install chromedriver manually from: https://sites.google.com/chromium.org/driver/getting-started
echo Place chromedriver in a directory included in your PATH.

echo Installation partially complete for Windows. Follow manual steps above.
pause
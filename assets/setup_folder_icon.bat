@echo off
echo Setting up Dragon's Lair folder icon...
echo.

REM Get the current directory path
set "CURRENT_DIR=%~dp0"
set "ICON_PATH=%CURRENT_DIR%folder_icon.ico"

REM Update desktop.ini with the correct path
echo [.ShellClassInfo] > desktop.ini
echo IconResource=%ICON_PATH%,0 >> desktop.ini
echo [ViewState] >> desktop.ini
echo Mode= >> desktop.ini
echo Vid= >> desktop.ini
echo FolderType=Generic >> desktop.ini

REM Set folder attributes
echo Making folder a system folder...
attrib +s "pygame_organized"
echo Setting folder to read-only...
attrib +r "pygame_organized"

echo.
echo Folder icon setup complete!
echo You may need to refresh your file explorer to see the changes.
echo If the icon doesn't appear immediately, try:
echo 1. Right-click the folder
echo 2. Select "Properties"
echo 3. Click "Customize" tab
echo 4. Click "Change Icon"
echo 5. Browse to folder_icon.ico
echo.
pause 
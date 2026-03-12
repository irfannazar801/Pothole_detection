@echo off
REM Run Pothole Detection with WebSocket Support
REM This script starts the pothole detection system with WebSocket enabled

echo ========================================
echo Pothole Detection - WebSocket Mode
echo ========================================
echo.

REM Check if video path is provided
if "%1"=="" (
    echo Usage: run_websocket.bat [video_path]
    echo Example: run_websocket.bat videos/demo.mp4
    echo.
    echo Using default video: videos/demo.mp4
    set VIDEO_PATH=videos/demo.mp4
) else (
    set VIDEO_PATH=%1
)

echo Starting pothole detection with WebSocket...
echo Video: %VIDEO_PATH%
echo.
echo INSTRUCTIONS:
echo 1. Make sure your phone and PC are on the SAME WiFi network
echo 2. Note the IP address shown when the server starts
echo 3. Open the Pothole Detection app on your phone
echo 4. Tap "Connect to Server"
echo 5. Enter the IP address shown below
echo 6. Tap "Connect"
echo.
echo Press any key to start...
pause > nul

python run.py --websocket --video %VIDEO_PATH%

echo.
echo ========================================
echo Session ended
echo ========================================
pause

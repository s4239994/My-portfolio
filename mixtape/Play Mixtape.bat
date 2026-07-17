@echo off
cd /d "%~dp0"
java -jar dist\mixtape.jar
if errorlevel 1 (
    echo.
    echo Something went wrong. Make sure Java is installed: https://www.java.com/download/
    pause
)

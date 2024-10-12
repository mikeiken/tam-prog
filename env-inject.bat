@echo off
setlocal EnableDelayedExpansion

REM Load .env file and set environment variables
set "envFilePath=.env"

if exist %envFilePath% (
    for /f "usebackq tokens=1* delims==" %%a in ("%envFilePath%") do (
        set "name=%%a"
        set "value=%%b"
        set "!name!=!value!"
    )
) else (
    echo The .env file does not exist at path: %envFilePath%
    exit /b 1
)

REM Check if a command is provided as arguments
if "%*"=="" (
    echo No command provided. Please provide a command to run.
    exit /b 1
)

REM Join all arguments into a single command string and execute it
set "command=%*"
cmd /c %command%
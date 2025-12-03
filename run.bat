@echo off
chcp 65001
cls

echo ======================================================
echo       🤖 AutoBot 자동 매매 시스템 시작 도우미
echo ======================================================
echo.

:: 1. 파이썬 설치 확인
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [오류] Python이 설치되지 않았거나 경로(PATH) 설정이 안 되어 있습니다.
    echo 가이드 1번을 참고하여 Python을 먼저 설치해주세요.
    pause
    exit
)

echo [1/3] 필수 프로그램(라이브러리) 설치 및 업데이트 확인 중...
pip install -r requirements.txt
echo.

echo [2/3] 설정 파일 확인 중...
if not exist config.ini (
    echo [경고] config.ini 파일이 없습니다! 
    echo 프로그램을 종료하고 config.ini 파일을 먼저 확인해주세요.
    pause
    exit
)

echo [3/3] 봇 프로그램을 실행합니다!
echo (이 창을 끄면 봇도 종료됩니다. 최소화만 해두세요.)
echo.
echo ======================================================
echo             실행 로그 (Log)
echo ======================================================
echo.

python -m app.main

pause
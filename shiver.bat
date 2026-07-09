@echo off
cd /d "%~dp0"
chcp 65001 >nul 2>&1
mode con lines=42 cols=110
title Shiver Stealer Builder v2.0

:menu
cd /d "%~dp0"
chcp 65001 > nul
cls
echo.
echo                 _____ _     _ _    ____  _          _ _
echo                / ____| |   (_) |  / ___|| |__   ___| | |
echo               | (___ | |__  _| |_ \___ \| '_ \ / _ \ | |
echo                \___ \| '_ \| | __| ___) | | | |  __/ | |
echo                ____) | | | | | |_ |____/|_| |_|\___|_|_|
echo               |_____/|_| |_|_|\__|
echo.
echo            ╔══════════════════════════════════════════════════════╗
echo            ║                                                      ║
echo            ║   SHIVER - ULTIMATE MULTI-FEATURE STEALER v2.0      ║
echo            ║   44 Browsers | Discord | Crypto | Gaming           
echo            ║                                                      ║
echo            ╚══════════════════════════════════════════════════════╝
echo.
echo            ══════════════════════════════════════════════════════╗
echo            ║  [1] Launch Builder Menu                             ║
echo            ║  [2] Install Dependencies                            ║
echo            ║  [3] About Shiver                                    ║
echo            ║  [4] Exit                                            ║
echo            ╚══════════════════════════════════════════════════════╝
echo.
set /p choice=             [?] Select option: 

if /i "%choice%"=="1" (
    goto builder
) else if /i "%choice%"=="2" (
    goto deps
) else if /i "%choice%"=="3" (
    goto about
) else if /i "%choice%"=="4" (
    exit
) else (
    goto menu
)

:builder
cd /d "%~dp0"
cls
echo.
echo            ╔══════════════════════════════════════════════════════╗
echo            ║  Starting Shiver Builder...                          ║
echo            ══════════════════════════════════════════════════════╝
echo.
python builder.py
echo.
echo             Return to main menu...
timeout /t 2 >nul
goto menu

:deps
cd /d "%~dp0"
cls
echo.
echo            ╔══════════════════════════════════════════════════════╗
echo            ║  Installing Dependencies...                          ║
echo            ╚══════════════════════════════════════════════════════╝
echo.
python builder.py --install-deps
echo.
echo             Installing PyInstaller for EXE building...
pip install pyinstaller
echo.
echo             Dependencies check complete!
pause
goto menu

:about
cd /d "%~dp0"
cls
echo.
echo            ╔══════════════════════════════════════════════════════╗
echo            ║                                                      ║
echo            ║              SHIVER STEALER v2.0                    ║
echo            ║              Ultimate Multi-Feature Tool            ║
echo            ║                                                      ║
echo            ╚══════════════════════════════════════════════════════╝
echo.
echo             Features:
echo             * 44 Browser Support (Chrome/Firefox/Opera/Edge etc.)
echo             * Discord Token Stealing (17+ clients including Vesktop)
echo             * Crypto Wallet Stealing (MetaMask, Exodus, 60+ wallets)
echo             * Gaming: Steam, Minecraft, Roblox
echo             * Instagram Session Stealing
echo             * Telegram Session Stealing
echo             * System Info / Screenshot / Wi-Fi
echo             * Full File System Search (interesting files)
echo             * Anti-VM / Anti-Debug
echo             * Custom Fake Error Message
echo             * Startup Persistence
echo             * Code Obfuscation (marshal+zlib+base64)
echo             * Clean Discord Webhook Output
echo             * Browser History Extraction
echo             * SSH Connections Grabbing (PuTTY, KiTTY, WinSCP)
echo             * Web3 Wallet Extensions (60+ wallets)
echo.
echo            ╔══════════════════════════════════════════════════════╗
pause
goto menu

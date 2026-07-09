@echo off

cd /d "%~dp0"

chcp 65001 >nul 2>&1

mode con lines=42 cols=110

title Shiver Stealer Builder



:menu

cls

echo.

echo                 SSSSS  H   H  IIIII  V   V  EEEEE  RRRR

echo                 S      H   H    I    V   V  E      R   R

echo                 SSS    HHHHH    I    V   V  EEE    RRRR

echo                    S   H   H    I     V V   E      R  R

echo                 SSSS   H   H  IIIII    V    EEEEE  R   R

echo.

echo            ==================================================

echo              SHIVER - ULTIMATE MULTI-STEALER

echo              45 Browsers ^| Discord ^| Crypto ^| Gaming

echo            ==================================================

echo.

echo            ==================================================

echo            [1] Launch Builder Menu

echo            [2] Install Dependencies

echo            [3] About Shiver

echo            [4] Exit

echo            ==================================================

echo.

set /p choice=             [?] Select option: 



if /i "%choice%"=="1" goto builder

if /i "%choice%"=="2" goto deps

if /i "%choice%"=="3" goto about

if /i "%choice%"=="4" goto exit_script

goto menu



:builder

cls

echo.

echo            ==================================================

echo              Starting Shiver Builder...

echo            ==================================================

echo.

python builder.py

echo.

pause

goto menu



:deps

cls

echo.

echo            ==================================================

echo              Installing Dependencies...

echo            ==================================================

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

cls

echo.

echo            ==================================================

echo                       SHIVER STEALER

echo            ==================================================

echo.

echo             Features:

echo             * 45 Browser Support (Chrome/Firefox/Opera/Edge etc.)

echo             * Discord Token Stealing (19+ clients)

echo             * Crypto Wallet Stealing (60+ Web3, Exodus, Ledger)

echo             * Gaming: Steam, Minecraft, Roblox

echo             * Telegram Session Stealing

echo             * System Info / Screenshot / Wi-Fi

echo             * Full File System Search (interesting files)

echo             * Anti-VM / Anti-Debug

echo             * Custom Fake Error Message

echo             * Startup Persistence

echo             * Multi-Layer Code Obfuscation

echo             * Clean Discord Webhook Output

echo             * Browser History Extraction

echo             * SSH Connections Grabbing (PuTTY, KiTTY, WinSCP)

echo             * Web3 Wallet Extensions (60+ wallets)

echo.

echo            ==================================================

pause

goto menu



:exit_script

echo.

echo             Press any key to close...

pause >nul

exit


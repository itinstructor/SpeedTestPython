cd c:\temp

python -m nuitka ^
    --onefile ^
    --mingw64 ^
    --lto=no ^
    --enable-plugin=tk-inter ^
    --windows-console-mode=disable ^
    --windows-icon-from-ico=speedtest_logo.ico ^
    speedtest_gui.py
pause

rem    --windows-disable-console ^
cd c:\temp

python -m nuitka ^
    --onefile ^
    --mingw64 ^
    --lto=no ^
    --enable-plugin=tk-inter ^
    --output-filename=speedtest_gui.exe ^
    --windows-disable-console ^
    --windows-icon-from-ico=speed.ico ^
    speedtest_gui_4_random_server.py
pause
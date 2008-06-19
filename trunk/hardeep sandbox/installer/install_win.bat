@ECHO OFF
"$INSTALL_PATH\win32\python-2.5.2.msi" /passive /log "$INSTALL_PATH\python_install.log"
c:\Python25\python.exe "$INSTALL_PATH\post_install.py"  
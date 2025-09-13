del .\GalaxyTimer.exe
pyinstaller -w -F --hidden-import=pyttsx3 ./pyscript/galaxytimer.py -i Resources/icon/icon.ico
move .\dist\galaxytimer.exe .\GalaxyTimer.exe
rd /s /q .\dist
rd /s /q .\build
del .\galaxytimer.spec
pause

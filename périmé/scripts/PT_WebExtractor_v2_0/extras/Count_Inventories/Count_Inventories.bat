set homefolder=%~dp0

cd ..\..

call batch\set_paths.bat

python %homefolder%\Count_Inventories.py

pause
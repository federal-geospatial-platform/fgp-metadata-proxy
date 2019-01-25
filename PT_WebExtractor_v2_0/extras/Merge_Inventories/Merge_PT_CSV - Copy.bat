set homefolder=%~dp0

cd ..\..

call batch\set_paths.bat

python %homefolder%\Merge_PT_CSV.py

pause
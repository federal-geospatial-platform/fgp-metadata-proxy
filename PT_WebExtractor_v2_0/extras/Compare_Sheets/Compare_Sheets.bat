echo off

set home_folder=%cd%

for /f "tokens=2 delims== " %%i in ('ftype Python.File') do (
    set "reg_entry=%%i"
)

for %%i in (%reg_entry%) do (
	set "py_loc=%%~dpi"
)

SET "PATH=%PATH%;%py_loc%;%py_loc%\Scripts"

python Compare_Sheets.py

pause
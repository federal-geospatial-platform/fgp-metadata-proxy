echo off

set home_folder=%cd%

call batch\set_python_path.bat

pushd %~dp0..\webdrivers\browsermob-proxy-2.1.4
set ABS_PATH=%CD%
SET PATH=%PATH%;%ABS_PATH%

pushd %~dp0..\webdrivers\chromedriver_win32
set ABS_PATH=%CD%
SET PATH=%PATH%;%ABS_PATH%

pushd %~dp0..\webdrivers\geckodriver
set ABS_PATH=%CD%
SET PATH=%PATH%;%ABS_PATH%

pushd %~dp0..\webdrivers\IEDriverServer_x64_2.42.0
set ABS_PATH=%CD%
SET PATH=%PATH%;%ABS_PATH%

pushd %home_folder%
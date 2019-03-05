echo off

call batch\set_python_path.bat

set /p pkg="Which Python package would you like to install (BeautifulSoup, Selenium, Browsermob, Requests, PyPDF, all):"

echo %pkg%

if "%pkg%" == "" (
	echo Please enter a valid entry.
	pause
	exit
)

CALL :LoCase pkg

echo %pkg%

echo on

if %pkg% == "all" (
	pip install beautifulsoup
	pip install lxml
	pip install selenium
	pip install browsermob-proxy
	pip install requests
	pip install pypdf
)

if "%pkg%" == "beautifulsoup" (
	pip install beautifulsoup
	pip install lxml
)
if "%pkg%" == "selenium" (
	pip install selenium
)
if "%pkg%" == "browsermob" (
	pip install browsermob-proxy
)
if "%pkg%" == "requests" (
	pip install requests
)
if "%pkg%" == "pypdf" (
	pip install pypdf
)

cmd /k

GOTO:EOF

:LoCase
:: Subroutine to convert a variable VALUE to all lower case.
:: The argument for this subroutine is the variable NAME.
FOR %%i IN ("A=a" "B=b" "C=c" "D=d" "E=e" "F=f" "G=g" "H=h" "I=i" "J=j" "K=k" "L=l" "M=m" "N=n" "O=o" "P=p" "Q=q" "R=r" "S=s" "T=t" "U=u" "V=v" "W=w" "X=x" "Y=y" "Z=z") DO CALL SET "%1=%%%1:%%~i%%"
GOTO:EOF
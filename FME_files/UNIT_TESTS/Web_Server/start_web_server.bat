@ECHO ON
REM ===========================================================================
REM Start the web server used for mocking web requests
REM ===========================================================================

SET Repertoire=%~dp0
cd %Repertoire%

set FLASK_APP=web_server
REM Activate the virtual environment

C:\Users\dpilon\AppData\Local\Programs\Python\Python37\python.exe -m venv .venv
call .\.venv\Scripts\activate
pip install -r requirements.txt

REM
pip list
REM 
REM Start the flask server
flask run

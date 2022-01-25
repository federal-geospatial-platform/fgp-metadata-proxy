@ECHO ON
REM ===========================================================================
REM Start the web server used for mocking web requests
REM ===========================================================================

SET Repertoire=%~dp0
cd %Repertoire%

set FLASK_APP=web_server
REM Activate the virtual environment
call .\venv\Scripts\activate
REM
pip list
REM 
REM Start the flask server
flask run

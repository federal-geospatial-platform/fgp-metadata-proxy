REM ===========================================================================
REM Enable local variables 
REM ===========================================================================
SETLOCAL ENABLEDELAYEDEXPANSION

 
REM ===========================================================================
REM Allow accented characters
REM ===========================================================================
chcp 1252

REM ===========================================================================
REM Determine the directory where the.bat is located and place it  
REM in the directory above while keeping the original directory
REM ===========================================================================
SET Repertoire=%~dp0
SET Ctfolder=%Repertoire%\..\..\..\FME_Custom_Transformers\
PUSHD %Ctfolder%

REM Define FME transformer path
SET FME_USER_RESOURCE_DIR=%USERPROFILE%\Documents\FME

REM ===========================================================================
REM Create file name variable in relative mode.
REM ===========================================================================
SET NomApp=YT_GEOWEB_EXTRACTOR
SET fme=%FME2020%


SET UserProfileFmx="%FME_USER_RESOURCE_DIR%\Transformers\%NomApp%.fmx"

REM ===========================================================================
REM Initialization of the variable that contains the result of the execution
REM ===========================================================================
SET Statut=0

REM ===========================================================================
REM Copy FMX to Documents
REM ===========================================================================
COPY/Y %Ctfolder%\%NomApp%.fmx %UserProfileFmx%
SET Statut=%Statut%%ERRORLEVEL%

PUSHD %Repertoire%\..

REM Define sources

REM First FME call,creating FFS File.  
set test_number=1
set source=met\source1.ffs
set resultat1=met\resultat1.ffs
set resultat2=met\resultat2.ffs
set resultat3=met\resultat3.ffs
set log=met\log_%test_number%.log

IF EXIST %log% del %log%
IF EXIST %resultat1% del %resultat1%
IF EXIST %resultat2% del %resultat2%
IF EXIST %resultat3% del %resultat3%
%fme% met\metrique_yt_geoweb_extractor.fmw ^
--IN_FFS_FILE %source% ^
--OUT_FFS_FILE_1 %resultat1% ^
--OUT_FFS_FILE_2 %resultat2% ^
--OUT_FFS_FILE_3 %resultat3% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%

FIND "HTTP transfer summary - status code: 200" %log%
SET Statut=%Statut%%ERRORLEVEL%

@IF [%Statut%] EQU [0000] (
 @ECHO INFORMATION : Metric test passed
 @COLOR A0
 @SET CodeSortie=999999
) ELSE (
 @ECHO ERROR: Metric test failed
 @COLOR CF
 @SET CodeSortie=-1
)

REM ===========================================================================
REM We return the window to the starting directory
REM ===========================================================================
POPD
 
REM ===========================================================================
REM We pause so that the window does not close 
REM in case we have to double-click on the.bat to execute it.
REM ===========================================================================
PAUSE
COLOR
EXIT /B %CodeSortie%


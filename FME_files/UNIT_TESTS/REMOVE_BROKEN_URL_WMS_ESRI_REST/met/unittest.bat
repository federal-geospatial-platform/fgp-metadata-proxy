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
PUSHD %Repertoire%\..

REM Define FME transformer path
SET FME_USER_RESOURCE_DIR=%USERPROFILE%\Documents

REM ===========================================================================
REM Create file name variable in relative mode.
REM ===========================================================================
SET NomApp=REMOVE_BROKEN_URL_WMS_ESRI_REST
SET fme=%FME2019%

SET UserProfileFmx="%FME_USER_RESOURCE_DIR%\FME\Transformers\%NomApp%.fmx"
SET UserProfileFmxGitHub="%FME_USER_RESOURCE_DIR%\GitHub\fgp-metadata-proxy\FME_files\FME_Custom_Transformers\%NomApp%.fmx"

REM ===========================================================================
REM Initialization of the variable that contains the result of the execution
REM ===========================================================================
SET Statut=0

REM ===========================================================================
REM Copy FMX to Documents
REM ===========================================================================
COPY/Y fme\%NomApp%.fmx %UserProfileFmx%
SET Statut=%Statut%%ERRORLEVEL%

REM Define sources

REM First FME call,creating FFS File with four compliant data records
set test_number=1
SET source=met\source%test_number%.ffs
set etalon=met\etalon%test_number%.ffs
set resultat=met\resultat.ffs
set resultat_2=met\resultat_2.ffs
set log=met\log_%test_number%.log
set log_comp=met\log_comp_%test_number%.log

IF EXIST %log% del %log%
IF EXIST met\resultat.ffs DEL met\resultat.ffs
IF EXIST met\resultat_2.ffs DEL met\resultat_2.ffs
%fme% met\metrique_remove_broken_url_wms_esri_rest.fmw ^
--IN_FFS_FILE %source% ^
--LOG_FILE %log% ^
--OUT_FFS_FILE %resultat% ^
--OUT_FFS_FILE_2 %resultat_2% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison data output with the standard
IF EXIST %log_comp% del %log_comp%
%fme% met\Comparateur.fmw ^
--IN_ETALON_FILE %etalon% ^
--IN_RESULTAT_FILE %resultat% ^
--LOG_FILE %log_comp% 
SET Statut=%Statut%%ERRORLEVEL%

REM Second FME call,Testing for client side error management
set test_number=2
SET source=met\source%test_number%.ffs
set etalon=met\etalon%test_number%.ffs
set etalon_2=met\etalon%test_number%_2.ffs
set resultat=met\resultat.ffs
set resultat_2=met\resultat_2.ffs
set log=met\log_%test_number%.log
set log_comp=met\log_comp_%test_number%.log
set log_comp_2=met\log_comp_%test_number%_2.log

IF EXIST %log% del %log%
IF EXIST met\resultat.ffs DEL met\resultat.ffs
IF EXIST met\resultat_2.ffs DEL met\resultat_2.ffs

%fme% met\metrique_remove_broken_url_wms_esri_rest.fmw ^
--IN_FFS_FILE %source% ^
--OUT_FFS_FILE %resultat% ^
--OUT_FFS_FILE_2 %resultat_2% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%
FIND "Client side error.  Status code 400." %log%
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison data output with the standard
IF EXIST %log_comp% del %log_comp%
%fme% met\Comparateur.fmw ^
--IN_ETALON_FILE %etalon% ^
--IN_RESULTAT_FILE %resultat% ^
--LOG_FILE %log_comp% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison error output with the standard
IF EXIST %log_comp_2% del %log_comp_2%
%fme% met\Comparateur.fmw ^
--IN_ETALON_FILE %etalon_2% ^
--IN_RESULTAT_FILE %resultat_2% ^
--LOG_FILE %log_comp_2% 
SET Statut=%Statut%%ERRORLEVEL%

REM Third FME call,Testing for server error
set test_number=3
SET source=met\source%test_number%.ffs
set etalon=met\etalon%test_number%.ffs
set etalon_2=met\etalon%test_number%_2.ffs
set resultat=met\resultat.ffs
set resultat_2=met\resultat_2.ffs
set log=met\log_%test_number%.log
set log_comp=met\log_comp_%test_number%.log
set log_comp_2=met\log_comp_%test_number%_2.log

IF EXIST %log% del %log%
IF EXIST met\resultat.ffs DEL met\resultat.ffs
IF EXIST met\resultat_2.ffs DEL met\resultat_2.ffs

%fme% met\metrique_remove_broken_url_wms_esri_rest.fmw ^
--IN_FFS_FILE %source% ^
--OUT_FFS_FILE %resultat% ^
--OUT_FFS_FILE_2 %resultat_2% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%
FIND "Server side error." %log%
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison data output with the standard
IF EXIST %log_comp% del %log_comp%
%fme% met\Comparateur.fmw ^
--IN_ETALON_FILE %etalon% ^
--IN_RESULTAT_FILE %resultat% ^
--LOG_FILE %log_comp% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison error output with the standard
IF EXIST %log_comp_2% del %log_comp_2%
%fme% met\Comparateur.fmw ^
--IN_ETALON_FILE %etalon_2% ^
--IN_RESULTAT_FILE %resultat_2% ^
--LOG_FILE %log_comp_2% 
SET Statut=%Statut%%ERRORLEVEL%

COPY/Y %UserProfileFmxGitHub% %UserProfileFmx%
SET Statut=%Statut%%ERRORLEVEL%

@IF [%Statut%] EQU [0000000000000] (
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


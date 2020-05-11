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
SET FME_USER_RESOURCE_DIR=%USERPROFILE%\Documents\FME

REM ===========================================================================
REM Create file name variable in relative mode.
REM ===========================================================================
SET NomApp=MAPPING_ERROR_LIST_CREATOR
SET fme=%FME2019%


SET UserProfileFmx="%FME_USER_RESOURCE_DIR%\Transformers\%NomApp%.fmx"

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

REM first FME call, mapping error produced in progress code attribute values 
SET test_number=1
SET source=met\source%test_number%.ffs
SET etalon=met\etalon%test_number%.ffs
SET resultat=met\resultat.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log

IF EXIST %log% del %log%
IF EXIST met\resultat.ffs DEL met\resultat.ffs

%fme% met\metrique_mapping_error_list_creator.fmw ^
--IN_FFS_FILE %source% ^
--OUT_FFS_FILE %resultat% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison data output with the standard
IF EXIST %log_comp% del %log_comp%
%fme% met\Comparateur.fmw ^
--IN_ETALON_FILE %etalon% ^
--IN_RESULTAT_FILE %resultat% ^
--LOG_FILE %log_comp% 
SET Statut=%Statut%%ERRORLEVEL%

REM second FME call, mapping error produced in spatial type attribute values
SET test_number=2
SET source=met\source%test_number%.ffs
SET etalon=met\etalon%test_number%.ffs
SET resultat=met\resultat.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log

IF EXIST %log% del %log%
IF EXIST met\resultat.ffs DEL met\resultat.ffs

%fme% met\metrique_mapping_error_list_creator.fmw ^
--IN_FFS_FILE %source% ^
--OUT_FFS_FILE %resultat% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison data output with the standard
IF EXIST %log_comp% del %log_comp%
%fme% met\Comparateur.fmw ^
--IN_ETALON_FILE %etalon% ^
--IN_RESULTAT_FILE %resultat% ^
--LOG_FILE %log_comp% 
SET Statut=%Statut%%ERRORLEVEL%

REM third FME call, mapping error produced in update cycle attribute values

SET test_number=3
SET source=met\source%test_number%.ffs
SET etalon=met\etalon%test_number%.ffs
SET resultat=met\resultat.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log

IF EXIST %log% del %log%
IF EXIST met\resultat.ffs DEL met\resultat.ffs

%fme% met\metrique_mapping_error_list_creator.fmw ^
--IN_FFS_FILE %source% ^
--OUT_FFS_FILE %resultat% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison data output with the standard
IF EXIST %log_comp% del %log_comp%
%fme% met\Comparateur.fmw ^
--IN_ETALON_FILE %etalon% ^
--IN_RESULTAT_FILE %resultat% ^
--LOG_FILE %log_comp% 
SET Statut=%Statut%%ERRORLEVEL%

REM fourth FME call, mapping error produced in role attribute values

SET test_number=4
SET source=met\source%test_number%.ffs
SET etalon=met\etalon%test_number%.ffs
SET resultat=met\resultat.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log

IF EXIST %log% del %log%
IF EXIST met\resultat.ffs DEL met\resultat.ffs

%fme% met\metrique_mapping_error_list_creator.fmw ^
--IN_FFS_FILE %source% ^
--OUT_FFS_FILE %resultat% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison data output with the standard
IF EXIST %log_comp% del %log_comp%
%fme% met\Comparateur.fmw ^
--IN_ETALON_FILE %etalon% ^
--IN_RESULTAT_FILE %resultat% ^
--LOG_FILE %log_comp% 
SET Statut=%Statut%%ERRORLEVEL%

REM fifth FME call, mapping error produced in format attribute values

SET test_number=5
SET source=met\source%test_number%.ffs
SET etalon=met\etalon%test_number%.ffs
SET resultat=met\resultat.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log

IF EXIST %log% del %log%
IF EXIST met\resultat.ffs DEL met\resultat.ffs

%fme% met\metrique_mapping_error_list_creator.fmw ^
--IN_FFS_FILE %source% ^
--OUT_FFS_FILE %resultat% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison data output with the standard
IF EXIST %log_comp% del %log_comp%
%fme% met\Comparateur.fmw ^
--IN_ETALON_FILE %etalon% ^
--IN_RESULTAT_FILE %resultat% ^
--LOG_FILE %log_comp% 
SET Statut=%Statut%%ERRORLEVEL%

@IF [%Statut%] EQU [000000000000] (
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


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
SET NomApp=PYCSW_URL_MAPPER_NG
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

REM ============================================================================
REM ========================== TEST  #1   ======================================
REM ============================================================================
REM First FME call,creating FFS File with one data record

set test_number=1
set etalon=met\etalon%test_number%.ffs
set resultat=met\resultat%test_number%.ffs
set forced_pycsw_url=""
set feature_type=PyCSW_config
set in_csv_lookup_tables_dir=.\met
set pt_abbr=QC
set log=met\log_%test_number%.log
set log_comp=met\log_comp_%test_number%.log

IF EXIST %log% del %log%
IF EXIST met\resultat%test_number%.ffs DEL met\resultat%test_number%.ffs
%fme% met\metrique_pycsw_url_mapper_ng.fmw ^
--FORCED_PYCSW_URL %forced_pycsw_url% ^
--FEATURE_TYPE %feature_type% ^
--IN_CSV_LOOKUP_TABLES_DIR %in_csv_lookup_tables_dir% ^
--P-T_ABBR %pt_abbr% ^
--LOG_FILE %log% ^
--OUT_RESULT %resultat%
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison data output with the standard
IF EXIST %log_comp% del %log_comp%
%fme% met\Comparateur.fmw ^
--IN_ETALON_FILE %etalon% ^
--IN_RESULTAT_FILE %resultat% ^
--LOG_FILE %log_comp% 
SET Statut=%Statut%%ERRORLEVEL%


REM ============================================================================
REM ========================== TEST  #2   ======================================
REM ============================================================================
REM First FME call,creating FFS File with FORCED_PYCSW_URL

set test_number=2
set etalon=met\etalon%test_number%.ffs
set resultat=met\resultat%test_number%.ffs
set forced_pycsw_url=https://forced_pycsw_url
set feature_type=PyCSW_config
set in_csv_lookup_tables_dir=.\met
set pt_abbr=QC
set log=met\log_%test_number%.log
set log_comp=met\log_comp_%test_number%.log

IF EXIST %log% del %log%
IF EXIST met\resultat%test_number%.ffs DEL met\resultat%test_number%.ffs
%fme% met\metrique_pycsw_url_mapper_ng.fmw ^
--FORCED_PYCSW_URL %forced_pycsw_url% ^
--FEATURE_TYPE %feature_type% ^
--IN_CSV_LOOKUP_TABLES_DIR %in_csv_lookup_tables_dir% ^
--P-T_ABBR %pt_abbr% ^
--LOG_FILE %log% ^
--OUT_RESULT %resultat%
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison data output with the standard
IF EXIST %log_comp% del %log_comp%
%fme% met\Comparateur.fmw ^
--IN_ETALON_FILE %etalon% ^
--IN_RESULTAT_FILE %resultat% ^
--LOG_FILE %log_comp% 
SET Statut=%Statut%%ERRORLEVEL%


REM ============================================================================
REM ========================== TEST  #3   ======================================
REM ============================================================================
REM First FME call, Error unknown province

set test_number=3
set etalon=met\etalon%test_number%.ffs
set resultat=met\resultat%test_number%.ffs
set forced_pycsw_url=""
set feature_type=PyCSW_config
set in_csv_lookup_tables_dir=.\met
set pt_abbr=ZZ
set log=met\log_%test_number%.log
set log_comp=met\log_comp_%test_number%.log

IF EXIST %log% del %log%
IF EXIST met\resultat%test_number%.ffs DEL met\resultat%test_number%.ffs
%fme% met\metrique_pycsw_url_mapper_ng.fmw ^
--FORCED_PYCSW_URL %forced_pycsw_url% ^
--FEATURE_TYPE %feature_type% ^
--IN_CSV_LOOKUP_TABLES_DIR %in_csv_lookup_tables_dir% ^
--P-T_ABBR %pt_abbr% ^
--LOG_FILE %log% ^
--OUT_RESULT %resultat%
SET Statut=%Statut%%ERRORLEVEL%

REM No need to make the comparaison with the .\met\Comparateur.fmw
REM Try to find the error in the log file
FIND "ERROR: Unknown provider:" %log%
SET Statut=%Statut%%ERRORLEVEL%


@IF [%Statut%] EQU [00000010] (
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


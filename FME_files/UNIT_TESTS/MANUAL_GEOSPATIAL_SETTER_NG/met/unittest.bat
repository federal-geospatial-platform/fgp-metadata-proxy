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
SET NomApp=MANUAL_GEOSPATIAL_SETTER_NG
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
REM First FME call with nine data records.  Five geospatial.  Four nongeospatial.
set test_number=1
SET source=met\source%test_number%.ffs
set etalon1=met\etalon%test_number%.ffs
set resultat1=met\resultat1.ffs
set log=met\log_%test_number%.log
set log_comp=met\log_comp_%test_number%.log
set feature_type=manual_setter_1_ON
set in_csv_lookup_tables_dir=.\met
set pt_abbr=ON

IF EXIST %log% del %log%
IF EXIST met\resultat1.ffs DEL met\resultat1.ffs
%fme% met\metrique_manual_geospatial_setter_ng.fmw ^
--IN_FFS_FILE %source% ^
--OUT_FFS_FILE %resultat1% ^
--LOG_FILE %log% ^
--FEATURE_TYPE %feature_type% ^
--IN_CSV_LOOKUP_TABLES_DIR %in_csv_lookup_tables_dir% ^
--P-T_ABBR %pt_abbr% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison of geospatial data output with the standard
IF EXIST %log_comp% del %log_comp%
%fme% met\Comparateur.fmw ^
--IN_ETALON_FILE %etalon1% ^
--IN_RESULTAT_FILE %resultat1% ^
--LOG_FILE %log_comp% 
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


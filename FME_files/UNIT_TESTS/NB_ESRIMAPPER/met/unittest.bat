REM TEST 1: expected values
REM TEST 2: Invalid URLS  - feature output testing
REM TEST 3: Invalid URLS - Error log output testing
REM Test 4: Missing resources{} attribute
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
SET NomApp=NB_ESRIMAPPER
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

REM First FME call,creating FFS File with ten compliant data records, no expected error output
set test_number=1
SET source=met\source%test_number%.ffs
set etalon=met\etalon%test_number%.ffs
set lookup=met\NB_ESRIServicesUnitTestSource%test_number%.csv
set resultat=met\resultat.ffs
set log=met\log_%test_number%.log
set log_comp=met\log_comp_%test_number%.log

IF EXIST %log% del %log%
IF EXIST met\resultat.ffs DEL met\resultat.ffs
%fme% met\metrique_nb_esrimapper_featureResultat.fmw ^
--IN_FFS_FILE %source% ^
--OUT_FFS_FILE %resultat% ^
--LOOKUP_TABLE %lookup% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison data output with the standard
IF EXIST %log_comp% del %log_comp%
%fme% met\Comparateur.fmw ^
--IN_ETALON_FILE %etalon% ^
--IN_RESULTAT_FILE %resultat% ^
--LOG_FILE %log_comp% 
SET Statut=%Statut%%ERRORLEVEL%

REM Second FME call,testing for invalid url catching. 10 compliant records, invalid url in lookup table. testing FEATURE OUTPUT
set test_number=2
SET source=met\source%test_number%.ffs
set etalon=met\etalon%test_number%.ffs
set lookup=met\NB_ESRIServicesUnitTestSource%test_number%.csv
set resultat=met\resultat.ffs
set log=met\log_%test_number%.log
set log_comp=met\log_comp_%test_number%.log

IF EXIST %log% del %log%
IF EXIST met\resultat.ffs DEL met\resultat.ffs

%fme% met\metrique_nb_esrimapper_featureResultat.fmw ^
--IN_FFS_FILE %source% ^
--OUT_FFS_FILE %resultat% ^
--LOOKUP_TABLE %lookup% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison data output with the standard
IF EXIST %log_comp% del %log_comp%
%fme% met\Comparateur.fmw ^
--IN_ETALON_FILE %etalon% ^
--IN_RESULTAT_FILE %resultat% ^
--LOG_FILE %log_comp% 

SET Statut=%Statut%%ERRORLEVEL%

REM third FME call,testing for invalid url catching. 9 compliant records, 1 noncompliant records, 2 invalid url in lookup table.expecting 2 error outputs expected testing ERROR OUTPUT
set test_number=3
SET source=met\source%test_number%.ffs
set etalon=met\etalon%test_number%.ffs
set lookup=met\NB_ESRIServicesUnitTestSource%test_number%.csv
set resultat=met\resultat.ffs
set log=met\log_%test_number%.log
set log_comp=met\log_comp_%test_number%.log

IF EXIST %log% del %log%
IF EXIST met\resultat.ffs DEL met\resultat.ffs

%fme% met\metrique_nb_esrimapper_errorResultat.fmw ^
--IN_FFS_FILE %source% ^
--OUT_FFS_FILE %resultat% ^
--LOOKUP_TABLE %lookup% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison data output with the standard
IF EXIST %log_comp% del %log_comp%
%fme% met\Comparateur.fmw ^
--IN_ETALON_FILE %etalon% ^
--IN_RESULTAT_FILE %resultat% ^
--LOG_FILE %log_comp% 

SET Statut=%Statut%%ERRORLEVEL%

REM 4th FME call,testing for invalid url catching. 10 compliant records, invalid url in lookup table. no error output expected testing FEATURE OUTPUT
set test_number=4
SET source=met\source%test_number%.ffs
set etalon=met\etalon%test_number%.ffs
set lookup=met\NB_ESRIServicesUnitTestSource%test_number%.csv
set resultat=met\resultat.ffs
set log=met\log_%test_number%.log
set log_comp=met\log_comp_%test_number%.log

IF EXIST %log% del %log%
IF EXIST met\resultat.ffs DEL met\resultat.ffs

%fme% met\metrique_nb_esrimapper_featureResultat.fmw ^
--IN_FFS_FILE %source% ^
--OUT_FFS_FILE %resultat% ^
--LOOKUP_TABLE %lookup% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison data output with the standard
IF EXIST %log_comp% del %log_comp%
%fme% met\Comparateur.fmw ^
--IN_ETALON_FILE %etalon% ^
--IN_RESULTAT_FILE %resultat% ^
--LOG_FILE %log_comp% 

SET Statut=%Statut%%ERRORLEVEL%

REM FINAL TEST
@IF [%Statut%] EQU [0000000000] (
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


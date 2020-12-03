REM TEST 1: 10 total input features. 2 maps, 3 datasets, 2 in the remove table, and 2 non-spatial datasets. geospatial feature output (5 features)
REM TEST 2: Same inpuit as test 1. non-geospatial feature output (3 features)
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
SET NomApp=SocrataAPICaller
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

REM TEST 1: 10 total input features. 2 maps, 3 datasets, 2 in the remove table, and 2 non-spatial datasets. geospatial feature output (5 features)
set test_number=1
SET source=met\source%test_number%.ffs
set etalon=met\etalon%test_number%.ffs
set lookupGeoData=met\geoDataTypes.csv
set lookupRemove=met\removeLookup.csv
set resultat=met\resultat.ffs
set socrataDomain=gnb.socrata.com
set AppToken=FL3Cxsebg0Vf6JQ0CnbMujHkQ
set unitTestMode=Yes
set log=met\log_%test_number%.log
set log_comp=met\log_comp_%test_number%.log

IF EXIST %log% del %log%
IF EXIST met\resultat.ffs DEL met\resultat.ffs
%fme% met\metrique_SocrataAPICaller_geofeatureResultat.fmw ^
--IN_FFS_FILE %source% ^
--OUT_FFS_FILE %resultat% ^
--LOOKUP_TABLE_GEODATATYPES %lookupGeoData% ^
--LOOKUP_TABLE_REMOVE %lookupRemove% ^
--UNIT_TEST %unitTestMode% ^
--SocrataAppToken  %AppToken% ^
--Socrata_Domain %socrataDomain% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison data output with the standard
IF EXIST %log_comp% del %log_comp%
%fme% met\Comparateur.fmw ^
--IN_ETALON_FILE %etalon% ^
--IN_RESULTAT_FILE %resultat% ^
--LOG_FILE %log_comp% 
SET Statut=%Statut%%ERRORLEVEL%

REM TEST 2: Same inpuit as test 1. non-geospatial feature output (3 features)
set test_number=2
SET source=met\source%test_number%.ffs
set etalon=met\etalon%test_number%.ffs
set lookupGeoData=met\geoDataTypes.csv
set lookupRemove=met\removeLookup.csv
set resultat=met\resultat.ffs
set socrataDomain=gnb.socrata.com
set AppToken=FL3Cxsebg0Vf6JQ0CnbMujHkQ
set unitTestMode=Yes
set log=met\log_%test_number%.log
set log_comp=met\log_comp_%test_number%.log

IF EXIST %log% del %log%
IF EXIST met\resultat.ffs DEL met\resultat.ffs
%fme% met\metrique_SocrataAPICaller_nonGeofeatureResultat.fmw ^
--IN_FFS_FILE %source% ^
--OUT_FFS_FILE %resultat% ^
--LOOKUP_TABLE_GEODATATYPES %lookupGeoData% ^
--LOOKUP_TABLE_REMOVE %lookupRemove% ^
--UNIT_TEST %unitTestMode% ^
--SocrataAppToken  %AppToken% ^
--Socrata_Domain %socrataDomain% ^
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
@IF [%Statut%] EQU [000000] (
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


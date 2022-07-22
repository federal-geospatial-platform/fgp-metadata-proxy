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
SET Ctfolder=%Repertoire%\..\..\..\FME_Workspaces\
PUSHD %Ctfolder%

REM Define FME transformer path
SET FME_USER_RESOURCE_DIR=%USERPROFILE%\Documents\FME

REM ===========================================================================
REM ================== Choose a PT to process =================================
REM ===========================================================================

echo off
:begin
echo - 
echo Select a PT for the metric processus:
echo ================================
echo -
echo 1) British Columbia (BC).
echo 2) Newfound Land And Labrodor (NL)

echo -
set /p op=Select a PT (number):
SET pt_abbr=""
if "%op%"=="1" SET pt_abbr=BC
if "%op%"=="2" SET pt_abbr=NL
if "%pt_abbr%"=="" echo Invalid choice (select a number)
if "%pt_abbr%"=="" goto begin
echo on

REM ===========================================================================
REM Create file name variable in relative mode.
REM ===========================================================================
SET Nom_Pt_App=%pt_abbr%_PROD
SET fme=%FME2020%

REM ===========================================================================
REM Initialization of the variable that contains the result of the execution
REM ===========================================================================
SET Statut=0

REM ===========================================================================
REM Copy FMW to Documents
REM ===========================================================================
PUSHD %Repertoire%\..
IF EXIST .\met\%Nom_Pt_App%.fmw del .\met\%Nom_Pt_App%.fmw
COPY/Y %Ctfolder%%Nom_Pt_App%.fmw .\met\%Nom_Pt_App%.fmw
SET Statut=%Statut%%ERRORLEVEL%
REM Define sources

REM ============================================================================
REM ========================== Set variables ===================================
REM ============================================================================

set xml_etalon=met\ETALON\%pt_abbr%\XML_LOCAL\*.xml
set xml_resultat=met\PT_HARVESTER\%pt_abbr%\XML_LOCAL\*.xml
set json_etalon=met\ETALON\%pt_abbr%\JSON_LOCAL\*.json
set json_resultat=met\PT_HARVESTER\%pt_abbr%\JSON_LOCAL\*.json
set logs=met\PT_HARVESTER\%pt_abbr%\LOG\*.log
set log=met\PT_HARVESTER\%pt_abbr%\LOG\%pt_abbr%.log
set log_1=%pt_abbr%_1.log
set log_2=%pt_abbr%_2.log
set log_comp=met\PT_HARVESTER\%pt_abbr%\LOG\%pt_abbr%_comp.log
set in_ffs_testing_file=.\met\SOURCE\%pt_abbr%_catalogue_subset.ffs
set in_out_working_dir=.\met\PT_HARVESTER

REM =============================================================================
REM ======================== Delete files =======================================
REM =============================================================================
IF EXIST %xml_resultat% del %xml_resultat%
IF EXIST %json_resultat% del %json_resultat%
IF EXIST %logs% del %logs%

REM ============================================================================
REM ========================== TEST # 1 Load XML and JSON files ================
REM ============================================================================

%fme% met\%Nom_Pt_App%.fmw ^
--ACTIVATE_GEO Yes ^
--ACTIVATE_NON_GEO Yes ^
--ACTIVATE_TRANSLATION No ^
--CATALOGUE_READER_SELECT No ^
--FORCED_PYCSW_URL "" ^
--IN_FFS_TESTING_FILE %in_ffs_testing_file% ^
--LOCAL_SOURCE_METADATA_DELTA_FINDER Yes ^
--LOCAL_WRITER Yes ^
--PT_ABBR %pt_abbr% ^
--METADATA_OVERWRITE Yes ^
--IN_OUT_WORKING_DIR %in_out_working_dir% ^
--SAMPLE_SIZE 0 ^
--URL_VALIDATION No

SET Statut=%Statut%%ERRORLEVEL%

REM Rename the FME log
ren %log% %log_1%

REM ===============================================================================
REM ==================== Comparison with the standard =============================
REM ===============================================================================

IF EXIST %log_comp% del %log_comp%
%fme% met\Comparateur.fmw ^
--XML_ETALON %xml_etalon% ^
--XML_RESULTAT %xml_resultat% ^
--JSON_ETALON %json_etalon% ^
--JSON_RESULTAT %json_resultat% ^
--LOG_FILE %log_comp% 
SET Statut=%Statut%%ERRORLEVEL%

REM ============================================================================
REM ========== TEST # 2 METADATA_OVERWRITE = No ==> No file written
REM ============================================================================
set xml_etalon=met\ETALON\%pt_abbr%\XML_LOCAL\*.xml
set xml_resultat=met\PT_HARVESTER\%pt_abbr%\XML_LOCAL\*.xml
set json_etalon=met\ETALON\%pt_abbr%\JSON_LOCAL\*.json
set json_resultat=met\PT_HARVESTER\%pt_abbr%\JSON_LOCAL\*.json
set log=met\PT_HARVESTER\%pt_abbr%\LOG\%pt_abbr%.log
set log_comp=met\PT_HARVESTER\%pt_abbr%\LOG\%pt_abbr%_comp.log
set in_ffs_testing_file=.\met\SOURCE\%pt_abbr%_catalogue_subset.ffs
set in_out_working_dir=.\met\PT_HARVESTER


%fme% met\%Nom_Pt_App%.fmw ^
--ACTIVATE_GEO Yes ^
--ACTIVATE_NON_GEO Yes ^
--ACTIVATE_TRANSLATION No ^
--CATALOGUE_READER_SELECT No ^
--FORCED_PYCSW_URL "" ^
--IN_FFS_TESTING_FILE %in_ffs_testing_file% ^
--LOCAL_SOURCE_METADATA_DELTA_FINDER Yes ^
--LOCAL_WRITER Yes ^
--PT_ABBR %pt_abbr% ^
--METADATA_OVERWRITE No ^
--IN_OUT_WORKING_DIR %in_out_working_dir% ^
--SAMPLE_SIZE 0 ^
--URL_VALIDATION No

SET Statut=%Statut%%ERRORLEVEL%

FIND "Total Features Written                                                       0" %log%
SET Statut=%Statut%%ERRORLEVEL%

REM Rename the FME log
ren %log% %log_2%

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


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
SET NomApp=YT_CATALOGUE_READER
SET fme=%FME2019%


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
set source1=met\source1.ffs
set source2=met\source2.ffs
set etalon1=met\etalon1.ffs
set etalon2=met\etalon2.ffs
set etalon3=met\etalon3.ffs
set resultat1=met\resultat1.ffs
set resultat2=met\resultat2.ffs
set resultat3=met\resultat3.ffs
set log=met\log_%test_number%.log
set log_comp_1=met\log_comp_1.log
set log_comp_2=met\log_comp_2.log
set log_comp_3=met\log_comp_3.log
set unit_test_activate=Yes

IF EXIST %log% del %log%
IF EXIST %resultat1% del %resultat1%
IF EXIST %resultat2% del %resultat2%
IF EXIST %resultat3% del %resultat3%
%fme% met\metrique_yt_catalogue_reader.fmw ^
--IN_FFS_FILE_1 %source1% ^
--IN_FFS_FILE_2 %source2% ^
--OUT_FFS_FILE_1 %resultat1% ^
--OUT_FFS_FILE_2 %resultat2% ^
--OUT_FFS_FILE_3 %resultat3% ^
--UNIT_TEST_ACTIVATE %unit_test_activate% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison with the standard
IF EXIST %log_comp_1% del %log_comp_1%
%fme% met\Comparateur.fmw ^
--IN_ETALON_FILE %etalon1% ^
--IN_RESULTAT_FILE %resultat1% ^
--LOG_FILE %log_comp_1% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison with the standard
IF EXIST %log_comp_2% del %log_comp_2%
%fme% met\Comparateur.fmw ^
--IN_ETALON_FILE %etalon2% ^
--IN_RESULTAT_FILE %resultat2% ^
--LOG_FILE %log_comp_2% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison with the standard
IF EXIST %log_comp_3% del %log_comp_3%
%fme% met\Comparateur.fmw ^
--IN_ETALON_FILE %etalon3% ^
--IN_RESULTAT_FILE %resultat3% ^
--LOG_FILE %log_comp_3% 
SET Statut=%Statut%%ERRORLEVEL%

FIND "'result' list atttribute missing from source data with unique name value yukon-landform-atlas.  Verify data with _response_body attribute in PROCESS_REPORT_MANUAL_TASKS .xlsx file in the project XLS folder" %log%
SET Statut=%Statut%%ERRORLEVEL%

@IF [%Statut%] EQU [0000000] (
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


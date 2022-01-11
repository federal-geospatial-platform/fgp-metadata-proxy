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
SET NomApp=METADATA_FORMAT_MAPPER
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
REM First FME call,creating FFS File with ten compliant data records

set test_number=1
SET source=met\source%test_number%.ffs
set etalon=met\etalon%test_number%.ffs
set lookup=met\FormatLookupUnitTest.csv
set resultat=met\resultat.ffs
set log=met\log_%test_number%.log
set log_comp=met\log_comp_%test_number%.log
SET att_to_map=resources{}.format
SET error_not_mapped=YES
SET real_value_refresh=YES
SET res_type_en_refresh=YES
SET res_type_fr_refresh=YES

IF EXIST %log% del %log%
IF EXIST met\resultat.ffs DEL met\resultat.ffs
%fme% met\metrique_metadata_format_mapper.fmw ^
--ATT_TO_MAP %att_to_map% ^
--ERROR_NOT_MAPPED %error_not_mapped% ^
--REAL_VALUE_REFRESH %real_value_refresh% ^
--RES_TYPE_EN_REFRESH %res_type_en_refresh% ^
--RES_TYPE_FR_REFRESH %res_type_fr_refresh% ^
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

REM ============================================================================
REM ========================== TEST  #2   ======================================
REM ============================================================================
REM Second FME call,Testing for client side error management
set test_number=2
SET source=met\source%test_number%.ffs
set etalon=met\etalon%test_number%.ffs
set lookup=met\FormatLookupUnitTest.csv
set resultat=met\resultat.ffs
set log=met\log_%test_number%.log
set log_comp=met\log_comp_%test_number%.log
SET att_to_map=resources{}.format
SET error_not_mapped=YES
SET real_value_refresh=YES
SET res_type_en_refresh=YES
SET res_type_fr_refresh=YES

IF EXIST %log% del %log%
IF EXIST met\resultat.ffs DEL met\resultat.ffs

%fme% met\metrique_metadata_format_mapper.fmw ^
--ATT_TO_MAP %att_to_map% ^
--ERROR_NOT_MAPPED %error_not_mapped% ^
--REAL_VALUE_REFRESH %real_value_refresh% ^
--RES_TYPE_EN_REFRESH %res_type_en_refresh% ^
--RES_TYPE_FR_REFRESH %res_type_fr_refresh% ^
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


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
SET NomApp=SPATIAL_TYPE_MAPPER
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


REM First FME call, full data set
set test_number=1
SET source=met\source%test_number%.ffs
set etalon=met\etalon%test_number%.ffs
set etalon2=met\etalon%test_number%_2.ffs
set resultat=met\resultat.ffs
set resultat2=met\resultat2.ffs
set lookup=met\UUID_Spatial_ON.xlsx
set log=met\log_%test_number%.log
set log_comp=met\log_comp_%test_number%.log

IF EXIST %log% del %log%
IF EXIST met\resultat.ffs DEL met\resultat.ffs
IF EXIST met\resultat2.ffs DEL met\resultat2.ffs 
%fme% met\metrique_spatial_type_mapper.fmw ^
--IN_FFS_FILE %source% ^
--OUT_FFS_FILE_1 %resultat% ^
--OUT_FFS_FILE_2 %resultat2% ^
--LOOKUP_TABLE %lookup% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison with the standard
IF EXIST %log_comp% del %log_comp%
%fme% met\Comparateur.fmw ^
--IN_ETALON_FILE %etalon% ^
--IN_RESULTAT_FILE %resultat% ^
--LOG_FILE %log_comp% 
SET Statut=%Statut%%ERRORLEVEL%

REM Second FME Call, full data set with one value missing from lookup table creating mapping error
set test_number=2
SET source=met\source1.ffs
set etalon=met\etalon%test_number%.ffs
set etalon2=met\etalon%test_number%_2.ffs
set resultat=met\resultat.ffs
set resultat2=met\resultat2.ffs
set lookup=met\UUID_Spatial_ON_2.xlsx
set log=met\log_%test_number%.log
set log_comp2=met\log_comp_%test_number%.log
set log_comp2_2=met\log_comp_%test_number%_2.log

IF EXIST %log% del %log%
IF EXIST met\resultat.ffs DEL met\resultat.ffs
IF EXIST met\resultat2.ffs DEL met\resultat2.ffs 
%fme% met\metrique_spatial_type_mapper.fmw ^
--IN_FFS_FILE %source% ^
--OUT_FFS_FILE_1 %resultat% ^
--OUT_FFS_FILE_2 %resultat2% ^
--LOOKUP_TABLE %lookup% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%
FIND "Data record with unique ID a763088c-018d-48b7-bf47-3027a8c725b8 missing from UUID_Spatial lookup table in SPATIAL_TYPE_MAPPER transformer and could not be mapped to a value." %log%
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison with the standard
IF EXIST %log_comp2% del %log_comp2%
%fme% met\Comparateur.fmw ^
--IN_ETALON_FILE %etalon% ^
--IN_RESULTAT_FILE %resultat% ^
--LOG_FILE %log_comp2% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison with the standard, error file
IF EXIST %log_comp2_2% del %log_comp2_2%
%fme% met\Comparateur.fmw ^
--IN_ETALON_FILE %etalon2% ^
--IN_RESULTAT_FILE %resultat2% ^
--LOG_FILE %log_comp2_2% 
SET Statut=%Statut%%ERRORLEVEL%

COPY/Y %UserProfileFmxGitHub% %UserProfileFmx%
SET Statut=%Statut%%ERRORLEVEL%

@IF [%Statut%] EQU [000000000] (
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


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
SET NomApp=UPDATE_TO_PROGRESS_MAPPER
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


REM First FME call, full data set.  Should throw no errors
set test_number=1
SET source=met\source%test_number%.ffs
set etalon=met\etalon%test_number%.ffs
set resultat=met\resultat.ffs
set resultat2=met\resultat2.ffs
set lookup=met\UpdateToProgress.csv
set log=met\log_%test_number%.log
set log_comp=met\log_comp_%test_number%.log

IF EXIST %log% del %log%
IF EXIST met\resultat.ffs DEL met\resultat.ffs
%fme% met\metrique_update_to_progress_mapper.fmw ^
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

REM Second FME Call, full data set with three values missing from lookup table creating mapping error
set test_number=2
SET source=met\source1.ffs
set etalon=met\etalon%test_number%.ffs
set etalon2=met\etalon%test_number%_2.ffs
set resultat=met\resultat.ffs
set resultat2=met\resultat2.ffs
set lookup=met\UpdateToProgress2.csv
set log=met\log_%test_number%.log
set log_comp2=met\log_comp_%test_number%.log
set log_comp2_2=met\log_comp_%test_number%_2.log


IF EXIST %log% del %log%
IF EXIST met\resultat.ffs DEL met\resultat.ffs
IF EXIST met\resultat2.ffs DEL met\resultat2.ffs 
%fme% met\metrique_update_to_progress_mapper.fmw ^
--IN_FFS_FILE %source% ^
--OUT_FFS_FILE_1 %resultat% ^
--OUT_FFS_FILE_2 %resultat2% ^
--LOOKUP_TABLE %lookup% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%

FIND "Data record with id value 218f6b93-e297-4429-9c48-d25cbbe5851e has resource_update_cycle attribute value Other not found in UpdateToProgress lookup table." %log%
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

@IF [%Statut%] EQU [00000000] (
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


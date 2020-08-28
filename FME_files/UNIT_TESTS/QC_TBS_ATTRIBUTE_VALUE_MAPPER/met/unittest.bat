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
SET NomApp=QC_TBS_ATTRIBUTE_VALUE_MAPPER
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


REM First FME call, source data with ten data records, one with a sector that is not in the lookup table.
set test_number=1
SET source=met\source%test_number%.ffs
set etalon=met\etalon%test_number%.ffs
set resultat=met\resultat.ffs
set lookup1=met\Format_TBS_QC.xlsx
set lookup2=met\UpdateFrequency_TBS_QC.xlsx
set lookup3=met\SubjectNTopic_TBS_QC.xlsx
set lookup4=met\ResourceType_TBS_QC.xlsx
set log=met\log_%test_number%.log
set log_comp=met\log_comp_%test_number%.log

IF EXIST %log% del %log%
IF EXIST met\resultat.ffs DEL met\resultat.ffs
%fme% met\metrique_qc_tbs_attribute_value_mapper.fmw ^
--IN_FFS_FILE %source% ^
--OUT_FFS_FILE %resultat% ^
--LOOKUP_TABLE_FORMAT %lookup1% ^
--LOOKUP_TABLE_FREQUENCY %lookup2% ^
--LOOKUP_TABLE_SUBJECT_TOPIC %lookup3% ^
--LOOKUP_TABLE_TYPE %lookup4% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%
FIND "Value XML not found in lookup table Format_TBS_QC in data record with id value d866cf2f-9a68-49ba-9825-41c9872d55cb" %log%
SET Statut=%Statut%%ERRORLEVEL%
FIND "Value sante not found in lookup table SubjectNTopic_TBS_QC in data record with id value e19082df-fd3e-43b0-83c7-78e5030667e2" %log%
SET Statut=%Statut%%ERRORLEVEL%
FIND "Value monthly not found in lookup table UpdateFrequency_TBS_QC in data record with id value 747d4c08-dbe8-4436-94e2-c7619321d5bd" %log%
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison with the standard
IF EXIST %log_comp% del %log_comp%
%fme% met\Comparateur.fmw ^
--IN_ETALON_FILE %etalon% ^
--IN_RESULTAT_FILE %resultat% ^
--LOG_FILE %log_comp% 
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


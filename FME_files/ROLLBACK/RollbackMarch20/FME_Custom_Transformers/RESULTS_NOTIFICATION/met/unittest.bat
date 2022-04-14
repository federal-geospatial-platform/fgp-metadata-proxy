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
SET NomApp=RESULTS_NOTIFICATION
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


REM First FME call to seven source ffs files that contain the following data ETL results: Records Inserted, Records Updated, Records Deleted Count, No Records Deleted Count, New Records Count, Updated Records Count and Total Records Count
set test_number=1
SET source_1=met\source1.ffs
SET source_2=met\source2.ffs
SET source_3=met\source3.ffs
SET source_4=met\source4.ffs
SET source_5=met\source5.ffs
SET source_6=met\source6.ffs
SET source_7=met\source7.ffs
set etalon=met\etalon1.ffs
set resultat=met\resultat.ffs
set log=met\log_%test_number%.log
set log_comp=met\log_comp_%test_number%.log

IF EXIST %log% del %log%
IF EXIST met\resultat.ffs DEL met\resultat.ffs
%fme% met\metrique_results_notification.fmw ^
--EMAIL_RESULTS No ^
--IN_FFS_FILE_1 %source_1% ^
--IN_FFS_FILE_2 %source_2% ^
--IN_FFS_FILE_3 %source_3% ^
--IN_FFS_FILE_4 %source_4% ^
--IN_FFS_FILE_5 %source_5% ^
--IN_FFS_FILE_6 %source_6% ^
--IN_FFS_FILE_7 %source_7% ^
--OUT_FFS_FILE %resultat% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%
FIND "TRANSLATION RESULTS: 4 new records were inserted into the CSW." %log%
SET Statut=%Statut%%ERRORLEVEL%
FIND "4 nouveaux enregistrements ont été insérés dans le CSW." %log%
SET Statut=%Statut%%ERRORLEVEL%
FIND "There were no new records that failed to insert into the CSW." %log%
SET Statut=%Statut%%ERRORLEVEL%
FIND "Il n'y a pas eu de nouveaux enregistrements qui n'ont pas été insérés dans le CSW." %log%
SET Statut=%Statut%%ERRORLEVEL%
FIND "18 existing records were updated in the CSW." %log%
SET Statut=%Statut%%ERRORLEVEL%
FIND "18 dossiers existants ont été mis à jour dans le CSW." %log%
SET Statut=%Statut%%ERRORLEVEL%
FIND "There were no existing records with updates that failed to load to the CSW." %log%
SET Statut=%Statut%%ERRORLEVEL%
FIND "Il n'y avait aucun enregistrement existant avec des mises à jour qui n'ont pas été chargées dans le CSW." %log%
SET Statut=%Statut%%ERRORLEVEL%
FIND "15 obsolete records were deleted from the CSW." %log%
SET Statut=%Statut%%ERRORLEVEL%
FIND "15 dossiers désuets ont été supprimés du CSW." %log%
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison with the standard
IF EXIST %log_comp% del %log_comp%
%fme% met\Comparateur.fmw ^
--IN_ETALON_FILE %etalon% ^
--IN_RESULTAT_FILE %resultat% ^
--LOG_FILE %log_comp% 
SET Statut=%Statut%%ERRORLEVEL%

@IF [%Statut%] EQU [00000000000000] (
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


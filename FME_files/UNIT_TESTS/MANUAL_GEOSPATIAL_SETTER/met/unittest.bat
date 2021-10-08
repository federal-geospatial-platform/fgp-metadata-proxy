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
SET NomApp=MANUAL_GEOSPATIAL_SETTER
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

REM First FME call with nine data records.  Five geospatial.  Four nongeospatial.
set test_number=1
SET source=met\source%test_number%.ffs
set etalon1=met\etalon%test_number%_1.ffs
set etalon2=met\etalon%test_number%_2.ffs
set resultat1=met\resultat1.ffs
set resultat2=met\resultat2.ffs
set resultat3=met\resultat3.ffs
set lookup=met\MANUAL_GEOSPATIAL_SETTER_TEST_%test_number%.xlsx
set log=met\log_%test_number%.log
set log_comp=met\log_comp_%test_number%.log

IF EXIST %log% del %log%
IF EXIST met\resultat1.ffs DEL met\resultat1.ffs
IF EXIST met\resultat2.ffs DEL met\resultat2.ffs
IF EXIST met\resultat3.ffs DEL met\resultat3.ffs
%fme% met\metrique_manual_geospatial_setter.fmw ^
--IN_FFS_FILE %source% ^
--IN_XLS_FILE %lookup% ^
--OUT_FFS_FILE %resultat1% ^
--OUT_FFS_FILE_2 %resultat2% ^
--OUT_FFS_FILE_3 %resultat3% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison of geospatial data output with the standard
IF EXIST %log_comp% del %log_comp%
%fme% met\Comparateur.fmw ^
--IN_ETALON_FILE %etalon1% ^
--IN_RESULTAT_FILE %resultat1% ^
--LOG_FILE %log_comp% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison of nongeospatial with the standard
IF EXIST %log_comp% del %log_comp%
%fme% met\Comparateur.fmw ^
--IN_ETALON_FILE %etalon2% ^
--IN_RESULTAT_FILE %resultat2% ^
--LOG_FILE %log_comp% 
SET Statut=%Statut%%ERRORLEVEL%

REM Second FME call with the same nine data records.  Five geospatial.  Four nongeospatial.  XLS file is missing one record throwing mapping warning.
set test_number=2
SET source=met\source1.ffs
set etalon1=met\etalon%test_number%_1.ffs
set etalon2=met\etalon%test_number%_2.ffs
set etalon3=met\etalon%test_number%_3.ffs
set resultat1=met\resultat1.ffs
set resultat2=met\resultat2.ffs
set resultat3=met\resultat3.ffs
set lookup=met\MANUAL_GEOSPATIAL_SETTER_TEST_%test_number%.xlsx
set log=met\log_%test_number%.log
set log_comp=met\log_comp_%test_number%.log

IF EXIST %log% del %log%
IF EXIST met\resultat1.ffs DEL met\resultat1.ffs
IF EXIST met\resultat2.ffs DEL met\resultat2.ffs
IF EXIST met\resultat3.ffs DEL met\resultat3.ffs
%fme% met\metrique_manual_geospatial_setter.fmw ^
--IN_FFS_FILE %source% ^
--IN_XLS_FILE %lookup% ^
--OUT_FFS_FILE %resultat1% ^
--OUT_FFS_FILE_2 %resultat2% ^
--OUT_FFS_FILE_3 %resultat3% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%
FIND "Data record with id fbdf77f1-096d-4985-bb3c-8a93956b1dec missing from UnmappedGeoData lookup table in MANUAL_GEOSPATIAL_SETTER transformer." %log%
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison of geospatial data output with the standard
IF EXIST %log_comp% del %log_comp%
%fme% met\Comparateur.fmw ^
--IN_ETALON_FILE %etalon1% ^
--IN_RESULTAT_FILE %resultat1% ^
--LOG_FILE %log_comp% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison of nongeospatial data output with the standard
IF EXIST %log_comp% del %log_comp%
%fme% met\Comparateur.fmw ^
--IN_ETALON_FILE %etalon2% ^
--IN_RESULTAT_FILE %resultat2% ^
--LOG_FILE %log_comp% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison of unmapped data record with the standard
IF EXIST %log_comp% del %log_comp%
%fme% met\Comparateur.fmw ^
--IN_ETALON_FILE %etalon3% ^
--IN_RESULTAT_FILE %resultat3% ^
--LOG_FILE %log_comp% 
SET Statut=%Statut%%ERRORLEVEL%

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


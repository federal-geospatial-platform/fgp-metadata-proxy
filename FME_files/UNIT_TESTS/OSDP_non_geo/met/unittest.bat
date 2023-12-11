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
PUSHD %Repertoire%\..\..\..


REM echo %cd%



REM ===========================================================================
REM Create file name variable in relative mode.
REM ===========================================================================
SET NomApp=OSDP_non_geo_dev
SET fme=%FME2020%
SET fmw=FME_Workspaces\%NomApp%.fmw
Set ComparateurBD=UNIT_TESTS\OSDP_non_geo\met\comparateur_sqllite.fmw
SET ComparateurCsv=UNIT_TESTS\OSDP_non_geo\met\comparateur_csv.fmw
set metdir=UNIT_TESTS\OSDP_non_geo\met










REM ===========================================================================
REM Initialization of the variable that contains the result of the execution
REM ===========================================================================
SET Statut=0




REM TEST #1 , exécution du programme pour une première fois avec 2 fichiers par province et un faux fichier pour ON.
SET no_test=1
SET log=%metdir%\log_%no_test%.log
SET working_dir=%metdir%\source%no_test%

REM Copie du template de db

COPY /Y %metdir%\template.db  %metdir%\bd_%no_test%.db
SET Statut=%Statut%%ERRORLEVEL%

REM Exécution du programme FME
IF EXIST %log% DEL %log%
%fme% %fmw% ^
--PROVIDER ALL ^
--IN_OUT_SQLLITE %metdir%\bd_%no_test%.db ^
--LOG_FILE %log% ^
--FME_SHAREDRESOURCE_DATA  %working_dir%
SET Statut=%Statut%%ERRORLEVEL%

pause
REM =============================================
REM Copier l'arborescence de traitement





pause

REM REM Define sources


REM REM First FME call,creating FFS File with fifteen compliant data records, ten of which require wms formatting
REM set test_number=1
REM SET source=met\source%test_number%.ffs
REM set etalon=met\etalon%test_number%.ffs
REM set resultat=met\resultat.ffs
REM set log=met\log_%test_number%.log
REM set log_comp=met\log_comp_%test_number%.log

REM IF EXIST %log% del %log%
REM IF EXIST met\resultat.ffs DEL met\resultat.ffs
REM %fme% met\metrique_bc_wms_formatter.fmw ^
REM --IN_FFS_FILE %source% ^
REM --OUT_FFS_FILE %resultat% ^
REM --LOG_FILE %log% 
REM SET Statut=%Statut%%ERRORLEVEL%

REM REM Comparison with the standard
REM IF EXIST %log_comp% del %log_comp%
REM %fme% met\Comparateur.fmw ^
REM --IN_ETALON_FILE %etalon% ^
REM --IN_RESULTAT_FILE %resultat% ^
REM --LOG_FILE %log_comp% 
REM SET Statut=%Statut%%ERRORLEVEL%

REM @IF [%Statut%] EQU [0000] (
 REM @ECHO INFORMATION : Metric test passed
 REM @COLOR A0
 REM @SET CodeSortie=999999
REM ) ELSE (
 REM @ECHO ERROR: Metric test failed
 REM @COLOR CF
 REM @SET CodeSortie=-1
REM )

REM REM ===========================================================================
REM REM We return the window to the starting directory
REM REM ===========================================================================
REM POPD
 
REM REM ===========================================================================
REM REM We pause so that the window does not close 
REM REM in case we have to double-click on the.bat to execute it.
REM REM ===========================================================================
REM PAUSE
REM COLOR
REM EXIT /B %CodeSortie%


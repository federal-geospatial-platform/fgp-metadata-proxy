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
SET ComparateurXlsx=UNIT_TESTS\OSDP_non_geo\met\comparateur_xlsx.fmw
set metdir=UNIT_TESTS\OSDP_non_geo\met










REM ===========================================================================
REM Initialization of the variable that contains the result of the execution
REM ===========================================================================
SET Statut=0


REM ===========================================================================
REM ===========================================================================
REM ====================      TEST #1     =====================================
REM 2 datasets par provider plus un faux fichier dans ontario
REM ===========================================================================

SET no_test=1
SET log=%metdir%\log_%no_test%.log
SET working_dir=%metdir%\source%no_test%
set etalon_dir=%metdir%\etalon%no_test%

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


REM Comparer la BD avec l'étalon
IF EXIST %log% DEL %log%
%fme% %ComparateurBD% ^
--IN_SQLLITE_RES_FILE %metdir%\bd_%no_test%.db ^
--IN_SQLLITE_ETALON_FILE %etalon_dir%\*.db ^
--LOG_FILE %log%
SET Statut=%Statut%%ERRORLEVEL%


REM Comparer le CSV avec l'étalon
IF EXIST %LOG% DEL %log% 
%fme% %ComparateurCsv% ^
--IN_CSV_RES_FILE %working_dir%\PT_Harvester\OSDP_geoDCAT\csv\*.csv ^
--IN_CSV_ETALON_FILE %etalon_dir%\*.csv ^
--LOG_FILE %log%
SET Statut=%Statut%%ERRORLEVEL%





REM ===========================================================================
REM ===========================================================================
REM ====================      TEST #2    =====================================
REM On utilise l'output du test 1 en relancant pour QC uniquement
REM ===========================================================================

SET no_test=2
SET log=%metdir%\log_%no_test%.log
REM Même working dir que test 1
SET working_dir=%metdir%\source1
set etalon_dir=%metdir%\etalon%no_test%





REM Exécution du programme FME
IF EXIST %log% DEL %log%
%fme% %fmw% ^
--PROVIDER QC ^
--IN_OUT_SQLLITE %metdir%\bd_1.db ^
--LOG_FILE %log% ^
--FME_SHAREDRESOURCE_DATA  %working_dir%
SET Statut=%Statut%%ERRORLEVEL%


REM Comparer la BD avec l'étalon
IF EXIST %log% DEL %log%
%fme% %ComparateurBD% ^
--IN_SQLLITE_RES_FILE %metdir%\bd_1.db ^
--IN_SQLLITE_ETALON_FILE %etalon_dir%\*.db ^
--LOG_FILE %log%
SET Statut=%Statut%%ERRORLEVEL%


REM Comparer le CSV avec l'étalon
IF EXIST %LOG% DEL %log% 
%fme% %ComparateurCsv% ^
--IN_CSV_RES_FILE %working_dir%\PT_Harvester\OSDP_geoDCAT\csv\*.csv ^
--IN_CSV_ETALON_FILE %etalon_dir%\*.csv ^
--LOG_FILE %log%
SET Statut=%Statut%%ERRORLEVEL%



REM ===========================================================================
REM ===========================================================================
REM ====================      TEST #3     =====================================
REM 1 fichier par provider, doit créer 12 updates et 12 delete
REM On continue avec des tests 1 et 2
REM ===========================================================================

SET no_test=3
SET log=%metdir%\log_%no_test%.log
SET working_dir=%metdir%\source%no_test%
set etalon_dir=%metdir%\etalon%no_test%




REM Exécution du programme FME
IF EXIST %log% DEL %log%
%fme% %fmw% ^
--PROVIDER ALL ^
--IN_OUT_SQLLITE %metdir%\bd_1.db ^
--LOG_FILE %log% ^
--FME_SHAREDRESOURCE_DATA  %working_dir%
SET Statut=%Statut%%ERRORLEVEL%


REM Comparer la BD avec l'étalon
IF EXIST %log% DEL %log%
%fme% %ComparateurBD% ^
--IN_SQLLITE_RES_FILE %metdir%\bd_1.db ^
--IN_SQLLITE_ETALON_FILE %etalon_dir%\*.db ^
--LOG_FILE %log%
SET Statut=%Statut%%ERRORLEVEL%


REM Comparer le CSV avec l'étalon pour les update
IF EXIST %LOG% DEL %log% 
%fme% %ComparateurCsv% ^
--IN_CSV_RES_FILE %working_dir%\PT_Harvester\OSDP_geoDCAT\csv\osdo_geodcat_*.csv ^
--IN_CSV_ETALON_FILE %etalon_dir%\geodcat.csv ^
--LOG_FILE %log%
SET Statut=%Statut%%ERRORLEVEL%

REM Comparer le CSV avec l'étalon pour les delete
IF EXIST %LOG% DEL %log% 
%fme% %ComparateurCsv% ^
--IN_CSV_RES_FILE %working_dir%\PT_Harvester\OSDP_geoDCAT\csv\osdp_delete.csv ^
--IN_CSV_ETALON_FILE %etalon_dir%\osdp_delete.csv ^
--LOG_FILE %log%
SET Statut=%Statut%%ERRORLEVEL%


REM ===========================================================================
REM ===========================================================================
REM ====================      TEST #4     =====================================
REM Aucun fichier par province, on doit avoir 24 deletes
REM ===========================================================================



SET no_test=4
SET log=%metdir%\log_%no_test%.log
SET working_dir=%metdir%\source%no_test%
set etalon_dir=%metdir%\etalon%no_test%




REM Exécution du programme FME
IF EXIST %log% DEL %log%
%fme% %fmw% ^
--PROVIDER ALL ^
--IN_OUT_SQLLITE %metdir%\bd_1.db ^
--LOG_FILE %log% ^
--FME_SHAREDRESOURCE_DATA  %working_dir%
SET Statut=%Statut%%ERRORLEVEL%


REM Comparer la BD avec l'étalon
IF EXIST %log% DEL %log%
%fme% %ComparateurBD% ^
--IN_SQLLITE_RES_FILE %metdir%\bd_1.db ^
--IN_SQLLITE_ETALON_FILE %etalon_dir%\*.db ^
--LOG_FILE %log%
SET Statut=%Statut%%ERRORLEVEL%




REM Comparer le CSV avec l'étalon pour les delete
IF EXIST %LOG% DEL %log% 
%fme% %ComparateurCsv% ^
--IN_CSV_RES_FILE %working_dir%\PT_Harvester\OSDP_geoDCAT\csv\osdp_delete.csv ^
--IN_CSV_ETALON_FILE %etalon_dir%\osdp_delete.csv ^
--LOG_FILE %log%
SET Statut=%Statut%%ERRORLEVEL%


REM ===========================================================================
REM ===========================================================================
REM ====================      TEST #5     =====================================
REM Un fichier plein d'erreur de corrélation pour AB
REM ===========================================================================



SET no_test=5
SET log=%metdir%\log_%no_test%.log
SET working_dir=%metdir%\source%no_test%
set etalon_dir=%metdir%\etalon%no_test%

REM Copie du template de db
COPY /Y %metdir%\template.db  %metdir%\bd_%no_test%.db

IF EXIST %working_dir%\PT_Harvester\OSDP_geoDCAT\XLS\*.xlsx DEL %working_dir%\PT_Harvester\OSDP_geoDCAT\XLS\*.xlsx

REM Exécution du programme FME
IF EXIST %log% DEL %log%
%fme% %fmw% ^
--PROVIDER AB ^
--IN_OUT_SQLLITE %metdir%\bd_%no_test%.db ^
--LOG_FILE %log% ^
--FME_SHAREDRESOURCE_DATA  %working_dir%
SET Statut=%Statut%%ERRORLEVEL%


REM Comparer le excel avec l'étalon
IF EXIST %LOG% DEL %log% 
%fme% %ComparateurXlsx% ^
--IN_XLSX_RES_FILE %working_dir%\PT_Harvester\OSDP_geoDCAT\xls\*.xlsx ^
--IN_XLSX_ETALON_FILE %etalon_dir%\*.xlsx ^
--LOG_FILE %log%
SET Statut=%Statut%%ERRORLEVEL%

@IF %Statut% EQU 0 (
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


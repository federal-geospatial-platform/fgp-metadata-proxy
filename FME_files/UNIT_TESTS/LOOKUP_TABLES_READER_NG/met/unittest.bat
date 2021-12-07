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
SET NomApp=LOOKUP_TABLES_READER_NG
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

REM Définition de la source 
REM Source 1
REM Une feature sur laquelle on a défini progress_code=COMPLETED, contact{0}.role=OWNER et contact{0}.role=USER

REM ============================================================================
REM ========================== TEST  #1   ======================================
REM ============================================================================
REM On test la lecture d'un lookup table avec le YAML associé
SET test_number=1
SET etalon=met\etalon_%test_number%.ffs
SET resultat=met\resultat_%test_number%.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log
SET feature_type=Update_%test_number%
SET csv_path=.\met
SET pt=QC

IF EXIST %log% del %log%
IF EXIST %resultat% DEL %resultat%
%fme% met\metrique_lookup_table_reader.fmw ^
--FEATURE_TYPE %feature_type% ^
--CSV_PATH %csv_path% ^
--PT %pt% ^
--OUT_FFS_FILE %resultat% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparaison avec l'étalon
IF EXIST %log_comp% del %log_comp%
%fme% met\Comparateur.fmw ^
--IN_FFS_ETALON_FILE %etalon% ^
--IN_FFS_RESULTAT_FILE %resultat% ^
--LOG_FILE %log_comp% 
SET Statut=%Statut%%ERRORLEVEL%

:deux
REM ============================================================================
REM ========================== TEST  #2   ======================================
REM ============================================================================
REM On test la lecture d'un lookup table avec le YAML associé
REM Le YAML applique plusieurs corrrection au fichier CSV
SET test_number=2
SET etalon=met\etalon_%test_number%.ffs
SET resultat=met\resultat_%test_number%.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log
SET feature_type=Update_%test_number%
SET csv_path=.\met
SET pt=QC

IF EXIST %log% del %log%
IF EXIST %resultat% DEL %resultat%
%fme% met\metrique_lookup_table_reader.fmw ^
--FEATURE_TYPE %feature_type% ^
--CSV_PATH %csv_path% ^
--PT %pt% ^
--OUT_FFS_FILE %resultat% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparaison avec l'étalon
IF EXIST %log_comp% del %log_comp%
%fme% met\Comparateur.fmw ^
--IN_FFS_ETALON_FILE %etalon% ^
--IN_FFS_RESULTAT_FILE %resultat% ^
--LOG_FILE %log_comp% 
SET Statut=%Statut%%ERRORLEVEL%


REM ============================================================================
REM ========================== TEST  #3   ======================================
REM ============================================================================
REM On test la lecture d'un lookup table pour une province avec le YAML associé
REM Le YAML applique plusieurs corrrection au fichier CSV
SET test_number=3
SET etalon=met\etalon_%test_number%.ffs
SET resultat=met\resultat_%test_number%.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log
SET feature_type=Update_%test_number%_QC
SET csv_path=.\met
SET pt=QC

IF EXIST %log% del %log%
IF EXIST %resultat% DEL %resultat%
%fme% met\metrique_lookup_table_reader.fmw ^
--FEATURE_TYPE %feature_type% ^
--CSV_PATH %csv_path% ^
--PT %pt% ^
--OUT_FFS_FILE %resultat% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparaison avec l'étalon
IF EXIST %log_comp% del %log_comp%
%fme% met\Comparateur.fmw ^
--IN_FFS_ETALON_FILE %etalon% ^
--IN_FFS_RESULTAT_FILE %resultat% ^
--LOG_FILE %log_comp% 
SET Statut=%Statut%%ERRORLEVEL%


REM ============================================================================
REM ========================== TEST  #4   ======================================
REM ============================================================================
REM On test la lecture d'un lookup table avec le YAML associé
REM Le YAML va détecter une erreur dans le fichier CSV (no_null)
SET test_number=4
SET etalon=met\etalon_%test_number%.ffs
SET resultat=met\resultat_%test_number%.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log
SET feature_type=Update_%test_number%
SET csv_path=.\met
SET pt=QC

IF EXIST %log% del %log%
IF EXIST %resultat% DEL %resultat%
%fme% met\metrique_lookup_table_reader.fmw ^
--FEATURE_TYPE %feature_type% ^
--CSV_PATH %csv_path% ^
--PT %pt% ^
--OUT_FFS_FILE %resultat% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%

FIND "Error: Column: real_value_english: No null error" %log%
SET Statut=%Statut%%ERRORLEVEL%


REM ============================================================================
REM ========================== TEST  #5   ======================================
REM ============================================================================
REM On test la lecture d'un lookup table avec le YAML associé
REM Les directives dans le YAML contiennent des fautes d'ortographes
SET test_number=5
SET etalon=met\etalon_%test_number%.ffs
SET resultat=met\resultat_%test_number%.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log
SET feature_type=Update_%test_number%
SET csv_path=.\met
SET pt=QC

IF EXIST %log% del %log%
IF EXIST %resultat% DEL %resultat%
%fme% met\metrique_lookup_table_reader.fmw ^
--FEATURE_TYPE %feature_type% ^
--CSV_PATH %csv_path% ^
--PT %pt% ^
--OUT_FFS_FILE %resultat% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%

FIND "Unknown YMAL directives: CSV_COLUMNS_err" %log%
SET Statut=%Statut%%ERRORLEVEL%


REM ============================================================================
REM ========================== TEST  #6   ======================================
REM ============================================================================
REM On test la lecture d'un lookup table avec le YAML associé
REM Le nom des colonnes est invalide i.e. ils ne correspondent pas avec le CSV
SET test_number=6
SET etalon=met\etalon_%test_number%.ffs
SET resultat=met\resultat_%test_number%.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log
SET feature_type=Update_%test_number%
SET csv_path=.\met
SET pt=QC

IF EXIST %log% del %log%
IF EXIST %resultat% DEL %resultat%
%fme% met\metrique_lookup_table_reader.fmw ^
--FEATURE_TYPE %feature_type% ^
--CSV_PATH %csv_path% ^
--PT %pt% ^
--OUT_FFS_FILE %resultat% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%

FIND "YAML column name in CSV_COLUMNS do not match CSV: real_value_english_err" %log% 
SET Statut=%Statut%%ERRORLEVEL%


REM ============================================================================
REM ========================== TEST  #7   ======================================
REM ============================================================================
REM On test la lecture d'un lookup table avec le YAML associé
REM Le nom des actions est invalide (inconnu)
SET test_number=7
SET etalon=met\etalon_%test_number%.ffs
SET resultat=met\resultat_%test_number%.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log
SET feature_type=Update_%test_number%
SET csv_path=.\met
SET pt=QC

IF EXIST %log% del %log%
IF EXIST %resultat% DEL %resultat%
%fme% met\metrique_lookup_table_reader.fmw ^
--FEATURE_TYPE %feature_type% ^
--CSV_PATH %csv_path% ^
--PT %pt% ^
--OUT_FFS_FILE %resultat% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%

FIND "YAML action is not known. Column: original_value; Action: lower_err" %log%
SET Statut=%Statut%%ERRORLEVEL%

REM ============================================================================
REM ========================== TEST  #8   ======================================
REM ============================================================================
REM On test la lecture d'un lookup table avec le YAML associé
REM Le nom des actions est invalide (inconnu)
SET test_number=8
SET etalon=met\etalon_%test_number%.ffs
SET resultat=met\resultat_%test_number%.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log
SET feature_type=Update_%test_number%
SET csv_path=.\met
SET pt=QC

IF EXIST %log% del %log%
IF EXIST %resultat% DEL %resultat%
%fme% met\metrique_lookup_table_reader.fmw ^
--FEATURE_TYPE %feature_type% ^
--CSV_PATH %csv_path% ^
--PT %pt% ^
--OUT_FFS_FILE %resultat% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%

FIND "Column: real_value_english: value: ANNUAL: Invalid domain" %log%
SET Statut=%Statut%%ERRORLEVEL%


:end
echo %Statut%
@IF [%Statut%] EQU [000000001010101010] (
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


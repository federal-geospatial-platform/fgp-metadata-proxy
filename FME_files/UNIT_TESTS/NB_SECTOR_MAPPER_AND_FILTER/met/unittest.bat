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
SET NomApp=NB_SECTOR_MAPPER_AND_FILTER
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
REM Une feature sur laquelle on a défini attribution=valid_sector et sector=valid_sector
REM Source 2
REM Une feature sur laquelle on a défini attribution=valid_sector et sector=nonvalid_sector
REM Source 3
REM Une feature sur laquelle on a défini attribution=nonvalid_sector et sector=valid_sector
REM Source 4
REM Une feature sur laquelle on a défini attribution=unknow_attribution et sector=valid_sector
REM Source 5
REM Une feature sur laquelle on a défini attribution=valid_sector et sector=unknow_sector

REM ============================================================================
REM ========================== TEST  #1   ======================================
REM ============================================================================
REM On test le mapping d'un feature avec sector/attribution valid
REM ============================================================================
SET test_number=1
SET source=met\source_%test_number%.ffs
SET etalon=met\etalon_123.ffs
SET lookup=met\lookuptables\Sector_Attribution_NB.csv
SET resultat=met\resultat_%test_number%.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log

IF EXIST %log% del %log%
IF EXIST %resultat% DEL %resultat%
%fme% met\metrique_NB_SECTOR_MAPPER_AND_FILTER.fmw ^
--IN_FFS_FILE %source% ^
--OUT_FFS_FILE %resultat% ^
--LOOKUP_TABLE %lookup% ^
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
REM ========================== TEST  #2   ======================================
REM ============================================================================
REM On test le mapping d'un feature avec sector non valid
REM ============================================================================
SET test_number=2
SET source=met\source_%test_number%.ffs
SET etalon=met\etalon_123.ffs
SET lookup=met\lookuptables\Sector_Attribution_NB.csv
SET resultat=met\resultat_%test_number%.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log

IF EXIST %log% del %log%
IF EXIST %resultat% DEL %resultat%
%fme% met\metrique_NB_SECTOR_MAPPER_AND_FILTER.fmw ^
--IN_FFS_FILE %source% ^
--OUT_FFS_FILE %resultat% ^
--LOOKUP_TABLE %lookup% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparaison avec l'étalon
IF EXIST %log_comp% del %log_comp%
%fme% met\Comparateur.fmw ^
--IN_FFS_ETALON_FILE %etalon% ^
--IN_FFS_RESULTAT_FILE %resultat% ^
--LOG_FILE %log_comp% 
SET Statut=%Statut%%ERRORLEVEL%

FIND "Feature with nonvalid_sector sector value and valid_sector attribution value has been filtered REASON=Federal dataset" %log%
SET Statut=%Statut%%ERRORLEVEL%



REM ============================================================================
REM ========================== TEST  #3   ======================================
REM ============================================================================
REM On test le mapping d'un feature avec attribution non valid
REM ============================================================================
SET test_number=3
SET source=met\source_%test_number%.ffs
SET etalon=met\etalon_123.ffs
SET lookup=met\lookuptables\Sector_Attribution_NB.csv
SET resultat=met\resultat_%test_number%.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log

IF EXIST %log% del %log%
IF EXIST %resultat% DEL %resultat%
%fme% met\metrique_NB_SECTOR_MAPPER_AND_FILTER.fmw ^
--IN_FFS_FILE %source% ^
--OUT_FFS_FILE %resultat% ^
--LOOKUP_TABLE %lookup% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparaison avec l'étalon
IF EXIST %log_comp% del %log_comp%
%fme% met\Comparateur.fmw ^
--IN_FFS_ETALON_FILE %etalon% ^
--IN_FFS_RESULTAT_FILE %resultat% ^
--LOG_FILE %log_comp% 
SET Statut=%Statut%%ERRORLEVEL%

FIND "Feature with valid_sector sector value and nonvalid_sector attribution value has been filtered REASON=Federal dataset" %log%
SET Statut=%Statut%%ERRORLEVEL%



REM ============================================================================
REM ========================== TEST  #4   ======================================
REM ============================================================================
REM On test le mapping d'un feature avec attribution unknown
REM ============================================================================
SET test_number=4
SET source=met\source_%test_number%.ffs
SET etalon=met\etalon_%test_number%.ffs
SET lookup=met\lookuptables\Sector_Attribution_NB.csv
SET resultat=met\resultat_%test_number%.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log

IF EXIST %log% del %log%
IF EXIST %resultat% DEL %resultat%
%fme% met\metrique_NB_SECTOR_MAPPER_AND_FILTER.fmw ^
--IN_FFS_FILE %source% ^
--OUT_FFS_FILE %resultat% ^
--LOOKUP_TABLE %lookup% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparaison avec l'étalon
IF EXIST %log_comp% del %log_comp%
%fme% met\Comparateur.fmw ^
--IN_FFS_ETALON_FILE %etalon% ^
--IN_FFS_RESULTAT_FILE %resultat% ^
--LOG_FILE %log_comp% 
SET Statut=%Statut%%ERRORLEVEL%

FIND "Attribute value unknown_attribution missing from Sector_Attribution_NB lookup table in NB_SECTOR_MAPPER_AND_FILTER transformer.  See PROCESS_REPORT_MANUAL_TASKS.xls file in NB/XLS directory for details." %log%
SET Statut=%Statut%%ERRORLEVEL%



REM ============================================================================
REM ========================== TEST  #5   ======================================
REM ============================================================================
REM On test le mapping d'un feature avec sector unknown
REM ============================================================================
SET test_number=5
SET source=met\source_%test_number%.ffs
SET etalon=met\etalon_%test_number%.ffs
SET lookup=met\lookuptables\Sector_Attribution_NB.csv
SET resultat=met\resultat_%test_number%.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log

IF EXIST %log% del %log%
IF EXIST %resultat% DEL %resultat%
%fme% met\metrique_NB_SECTOR_MAPPER_AND_FILTER.fmw ^
--IN_FFS_FILE %source% ^
--OUT_FFS_FILE %resultat% ^
--LOOKUP_TABLE %lookup% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparaison avec l'étalon
IF EXIST %log_comp% del %log_comp%
%fme% met\Comparateur.fmw ^
--IN_FFS_ETALON_FILE %etalon% ^
--IN_FFS_RESULTAT_FILE %resultat% ^
--LOG_FILE %log_comp% 
SET Statut=%Statut%%ERRORLEVEL%

FIND "Attribute value unknown_sector missing from Sector_Attribution_NB lookup table in NB_SECTOR_MAPPER_AND_FILTER transformer.  See PROCESS_REPORT_MANUAL_TASKS.xls file in NB/XLS directory for details." %log%
SET Statut=%Statut%%ERRORLEVEL%



REM ============================================================================
REM ========================== TEST  #ERREUR-1  ================================
REM ============================================================================
REM On test une lookup table sans attribut 'original_sector_value'
REM ============================================================================

SET test_number=ERREUR-1
SET lookup=met\lookuptables\%test_number%.csv
SET resultat=met\resultat_%test_number%.ffs
set source=met\source_1.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log

IF EXIST %log% del %log%
IF EXIST %resultat% DEL %resultat%
%fme% met\metrique_NB_SECTOR_MAPPER_AND_FILTER.fmw ^
--IN_FFS_FILE %source% ^
--OUT_FFS_FILE %resultat% ^
--LOOKUP_TABLE %lookup% ^
--LOG_FILE %log%  

FIND "Missing attribute values found in Sector_NB lookup table, NB_SECTOR_MAPPER_AND_FILTER transformer.  Translation terminated." %log%
SET Statut=%Statut%%ERRORLEVEL%



REM ============================================================================
REM ========================== TEST  #ERREUR-2  ================================
REM ============================================================================
REM On test une lookup table sans attribut 'sector_value_en'
REM ============================================================================

SET test_number=ERREUR-2
SET lookup=met\lookuptables\%test_number%.csv
SET resultat=met\resultat_%test_number%.ffs
set source=met\source_1.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log

IF EXIST %log% del %log%
IF EXIST %resultat% DEL %resultat%
%fme% met\metrique_NB_SECTOR_MAPPER_AND_FILTER.fmw ^
--IN_FFS_FILE %source% ^
--OUT_FFS_FILE %resultat% ^
--LOOKUP_TABLE %lookup% ^
--LOG_FILE %log%  

FIND "Missing attribute values found in Sector_NB lookup table, NB_SECTOR_MAPPER_AND_FILTER transformer.  Translation terminated." %log%
SET Statut=%Statut%%ERRORLEVEL%



REM ============================================================================
REM ========================== TEST  #ERREUR-3  ================================
REM ============================================================================
REM On test une lookup table sans attribut 'sector_value_fr'
REM ============================================================================

SET test_number=ERREUR-3
SET lookup=met\lookuptables\%test_number%.csv
SET resultat=met\resultat_%test_number%.ffs
set source=met\source_1.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log

IF EXIST %log% del %log%
IF EXIST %resultat% DEL %resultat%
%fme% met\metrique_NB_SECTOR_MAPPER_AND_FILTER.fmw ^
--IN_FFS_FILE %source% ^
--OUT_FFS_FILE %resultat% ^
--LOOKUP_TABLE %lookup% ^
--LOG_FILE %log%  

FIND "Missing attribute values found in Sector_NB lookup table, NB_SECTOR_MAPPER_AND_FILTER transformer.  Translation terminated." %log%
SET Statut=%Statut%%ERRORLEVEL%



REM ============================================================================
REM ========================== TEST  #ERREUR-4  ================================
REM ============================================================================
REM On test une lookup table sans attribut 'jurisdiction'
REM ============================================================================

SET test_number=ERREUR-4
SET lookup=met\lookuptables\%test_number%.csv
SET resultat=met\resultat_%test_number%.ffs
set source=met\source_1.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log

IF EXIST %log% del %log%
IF EXIST %resultat% DEL %resultat%
%fme% met\metrique_NB_SECTOR_MAPPER_AND_FILTER.fmw ^
--IN_FFS_FILE %source% ^
--OUT_FFS_FILE %resultat% ^
--LOOKUP_TABLE %lookup% ^
--LOG_FILE %log%  

FIND "Missing attribute values found in Sector_NB lookup table, NB_SECTOR_MAPPER_AND_FILTER transformer.  Translation terminated." %log%
SET Statut=%Statut%%ERRORLEVEL%



REM ============================================================================
REM ========================== TEST  #ERREUR-5  ================================
REM ============================================================================
REM On test une lookup table sans attribut 'fgp_publish'
REM ============================================================================

SET test_number=ERREUR-5
SET lookup=met\lookuptables\%test_number%.csv
SET resultat=met\resultat_%test_number%.ffs
set source=met\source_1.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log

IF EXIST %log% del %log%
IF EXIST %resultat% DEL %resultat%
%fme% met\metrique_NB_SECTOR_MAPPER_AND_FILTER.fmw ^
--IN_FFS_FILE %source% ^
--OUT_FFS_FILE %resultat% ^
--LOOKUP_TABLE %lookup% ^
--LOG_FILE %log%  

FIND "Missing attribute values found in Sector_NB lookup table, NB_SECTOR_MAPPER_AND_FILTER transformer.  Translation terminated." %log%
SET Statut=%Statut%%ERRORLEVEL%



REM ============================================================================
REM ========================== TEST  #ERREUR-6  ================================
REM ============================================================================
REM On test une lookup table avec sector doublon
REM ============================================================================

SET test_number=ERREUR-6
SET lookup=met\lookuptables\%test_number%.csv
SET resultat=met\resultat_%test_number%.ffs
set source=met\source_1.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log

IF EXIST %log% del %log%
IF EXIST %resultat% DEL %resultat%
%fme% met\metrique_NB_SECTOR_MAPPER_AND_FILTER.fmw ^
--IN_FFS_FILE %source% ^
--OUT_FFS_FILE %resultat% ^
--LOOKUP_TABLE %lookup% ^
--LOG_FILE %log%  

FIND "Duplicate feature valid_sector found in original_sector_value attribute in sector lookup table, Sector_NB transformer.  Translation terminated." %log%
SET Statut=%Statut%%ERRORLEVEL%



@IF [%Statut%] EQU [0000000000000000000000] (
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


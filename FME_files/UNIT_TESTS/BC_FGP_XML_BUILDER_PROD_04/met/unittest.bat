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
SET NomApp=BC_FGP_XML_BUILDER_PROD_04
SET fme=%FME2019%


SET UserProfileFmw="%FME_USER_RESOURCE_DIR%\workspaces\%NomApp%.fmw"

REM ===========================================================================
REM Initialization of the variable that contains the result of the execution
REM ===========================================================================
SET Statut=0

REM ===========================================================================
REM Copy FMW to Documents
REM ===========================================================================
COPY/Y fme\%NomApp%.fmw %UserProfileFmw%
SET Statut=%Statut%%ERRORLEVEL%

REM Define sources

REM First FME call,creating FFS File.  
set test_number=1
set source1=met\source1.ffs
set source2=met\source2.ffs
set etalon=met\etalon1.ffs
set resultat=met\resultat.ffs
set local=Yes
set lookup=met\P-T_ETL_LOOKUP_TABLES.xlsx
set log=met\log_%test_number%.log
set log_comp=met\log_comp_%test_number%.log
set translation=No
set catalogue=No 
set unittest=Yes

IF EXIST %log% del %log%
IF EXIST met\resultat.ffs DEL met\resultat.ffs
%fme% fme\BC_FGP_XML_BUILDER_PROD_04.fmw ^
--ACTIVATE_TRANSLATION %translation% ^
--CATALOGUE_READER_SELECT %catalogue% ^
--IN_FFS_CAT_READ_TEST_FILE %source2% ^
--IN_FFS_TESTING_FILE %source1% ^
--IN_XLS_LOOKUP_TABLE_FILE %lookup% ^
--LOCAL_WRITER %local% ^
--OUT_FFS_FILE %resultat% ^
--UNIT_TEST_SELECT %unittest% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%
FIND "Client side error.  Status code 400" %log%
SET Statut=%Statut%%ERRORLEVEL%
FIND "Data record with unique ID b1a97948-778d-4331-b202-762cff17f2b8 missing from UUID_Spatial lookup table in SPATIAL_TYPE_MAPPER transformer and could not be mapped to a value." %log%
SET Statut=%Statut%%ERRORLEVEL%
FIND "Attribute value TOTO missing from Geospatial lookup table in GEOSPATIAL_DATA_VALIDATOR transformer.  See PROCESS_REPORT_MANUAL_TASKS.xls file in XLS directory for details." %log%
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


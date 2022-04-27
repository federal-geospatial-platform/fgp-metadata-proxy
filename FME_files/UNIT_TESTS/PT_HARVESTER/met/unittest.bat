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
SET NomApp=QC_XML_BUILDER_PROD_7
SET fme=%FME2020%

REM ===========================================================================
REM Initialization of the variable that contains the result of the execution
REM ===========================================================================
SET Statut=0

REM ===========================================================================
REM Copy FMX to Documents
REM ===========================================================================
REM COPY/Y %Ctfolder%\%NomApp%.fmx .\metrique_pt_harvester_del.fmw
SET Statut=%Statut%%ERRORLEVEL%

PUSHD %Repertoire%\..

REM Define sources

REM ============================================================================
REM ========================== TEST  #1   ======================================
REM ============================================================================

set test_number=1
set source=met\QC_CKAN_READER_SUBSET.ffs
set xml_etalon=met\ETALON\QC\XML_LOCAL\*.xml
set xml_resultat=met\PT_HARVESTER\QC\XML_LOCAL\*.xml
set json_etalon=met\ETALON\QC\JSON_LOCAL\*.json
set json_resultat=met\PT_HARVESTER\QC\JSON_LOCAL\*.json
set etalon_json=met\etalon_json.ffs
set etalon_xml=met\etalon_xml.ffs
set resultat_json=met\resultat_json.ffs
set resultat_xml=met\resultat_xml.ffs
set log=met\log_QC.log
set log_comp=met\log_comp_QC.log

set activate_geo=Yes
set activate_non_geo=Yes
set activate_translation=No
set catalogue_reader_select=No
set forced_pycsw_url=""
set in_ffs_testing_file=%source%
set local_source_metadata_delta_finder=Yes
set local_writer=Yes
set pt_abbr=QC
set pycsw_ckan_overwrite=No
set in_out_working_dir=met\PT_HARVESTER
set sample_size=0

IF EXIST %log% del %log%
IF EXIST %resultat%.ffs DEL %resultat%.ffs
%fme% met\metrique_pt_harvester.fmw ^
--LOG_FILE %log% ^
--ACTIVATE_GEO %activate_geo% ^
--ACTIVATE_NON_GEO %activate_non_geo% ^
--ACTIVATE_TRANSLATION %activate_translation% ^
--FORCED_PYCSW_URL %forced_pycsw_url% ^
--IN_FFS_TESTING_FILE %in_ffs_testing_file% ^
--LOCAL_SOURCE_METADATA_DELTA_FINDER %local_source_metadata_delta_finder% ^
--LOCAL_WRITER %local_writer% ^
--P-T_ABBR %pt_abbr% ^
--PYCSW_CKAN_OVERWRITE %pycsw_ckan_overwrite% ^
--IN_OUT_WORKING_DIR %in_out_working_dir% ^
--SAMPLE_SIZE %sample_size%
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison with the standard
IF EXIST %log_comp% del %log_comp%
%fme% met\Comparateur.fmw ^
--XML_ETALON %xml_etalon% ^
--XML_RESULTAT %xml_resultat% ^
--JSON_ETALON %json_etalon% ^
--JSON_RESULTAT %json_resultat% ^
--LOG_FILE %log_comp% 
SET Statut=%Statut%%ERRORLEVEL%

@IF [%Statut%] EQU [0000] (
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


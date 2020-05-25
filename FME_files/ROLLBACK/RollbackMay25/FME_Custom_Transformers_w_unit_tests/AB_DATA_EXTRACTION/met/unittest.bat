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
SET NomApp=AB_DATA_EXTRACTION
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

REM First FME call, testing Alberta HTTP call to three URL's.  
set test_number=1
set source_1=met\source1.ffs
set source_2=met\source2.ffs
set source_3=met\source3.ffs
set source_4=met\source4.ffs
set resultat_1=met\resultat1.ffs
set resultat_2=met\resultat2.ffs
set resultat_3=met\resultat3.ffs
set resultat_4=met\resultat4.ffs
set log=met\log_%test_number%.log

IF EXIST %log% del %log%
IF EXIST %resultat_1% DEL %resultat_1%
IF EXIST %resultat_2% DEL %resultat_2%
IF EXIST %resultat_3% DEL %resultat_3%
IF EXIST %resultat_4% DEL %resultat_4%
%fme% met\metrique_ab_data_extraction.fmw ^
--CSW_QUERY_1 "https://geodiscover.alberta.ca/geoportal/csw?request=getRecords&service=CSW ..." ^
--CSW_QUERY_2 "https://geodiscover.alberta.ca/geoportal/csw?request=getRecords&service=CSW&resultType=results&ElementSetName=summary&startPosition=1" ^
--CSW_QUERY_3 "https://geodiscover.alberta.ca/geoportal/rest/metadata/item/a82d775c1dc841e4b0e61186531c0d8b/xml" ^
--ENTITY_SEARCH_LITERAL Alberta ^
--IN_FFS_FILE_1 %source_1% ^
--IN_FFS_FILE_2 %source_2% ^
--IN_FFS_FILE_3 %source_3% ^
--IN_FFS_FILE_4 %source_4% ^
--OUT_FFS_FILE_1 %resultat_1% ^
--OUT_FFS_FILE_2 %resultat_2% ^
--OUT_FFS_FILE_3 %resultat_3% ^
--OUT_FFS_FILE_4 %resultat_4% ^
--SAMPLE_SELECT Yes ^
--SAMPLE_SIZE 80 ^
--TIME_FILTER_DAYS 0 ^
--TIME_FILTER_MONTHS 24 ^
--TIME_STAMP 20200309 ^
--UNIT_TEST_HTTP_BYPASS No ^
--UNIT_TEST_PYCSW_BYPASS Yes ^
--LOG_FILE %log% 

FIND "First HTTP status code is 200" %log%
SET Statut=%Statut%%ERRORLEVEL%
FIND "Second HTTP status code is 200" %log%
SET Statut=%Statut%%ERRORLEVEL%
FIND "Third HTTP status code is 200" %log%
SET Statut=%Statut%%ERRORLEVEL%

REM Second FME call, testing Alberta HTTP call, inducing an error to the first URL. 
set test_number=2
set source_1=met\source1.ffs
set source_2=met\source2.ffs
set source_3=met\source3.ffs
set source_4=met\source4.ffs
set resultat_1=met\resultat1.ffs
set resultat_2=met\resultat2.ffs
set resultat_3=met\resultat3.ffs
set resultat_4=met\resultat4.ffs
set log=met\log_%test_number%.log

IF EXIST %log% del %log%
IF EXIST %resultat_1% DEL %resultat_1%
IF EXIST %resultat_2% DEL %resultat_2%
IF EXIST %resultat_3% DEL %resultat_3%
IF EXIST %resultat_4% DEL %resultat_4%
%fme% met\metrique_ab_data_extraction.fmw ^
--CSW_QUERY_1 "http://httpstat.us/500" ^
--CSW_QUERY_2 "https://geodiscover.alberta.ca/geoportal/csw?request=getRecords&service=CSW&resultType=results&ElementSetName=summary&startPosition=1" ^
--CSW_QUERY_3 "https://geodiscover.alberta.ca/geoportal/rest/metadata/item/a82d775c1dc841e4b0e61186531c0d8b/xml" ^
--ENTITY_SEARCH_LITERAL Alberta ^
--IN_FFS_FILE_1 %source_1% ^
--IN_FFS_FILE_2 %source_2% ^
--IN_FFS_FILE_3 %source_3% ^
--IN_FFS_FILE_4 %source_4% ^
--OUT_FFS_FILE_1 %resultat_1% ^
--OUT_FFS_FILE_2 %resultat_2% ^
--OUT_FFS_FILE_3 %resultat_3% ^
--OUT_FFS_FILE_4 %resultat_4% ^
--SAMPLE_SELECT Yes ^
--SAMPLE_SIZE 80 ^
--TIME_FILTER_DAYS 0 ^
--TIME_FILTER_MONTHS 24 ^
--TIME_STAMP 20200309 ^
--UNIT_TEST_HTTP_BYPASS No ^
--UNIT_TEST_PYCSW_BYPASS Yes ^
--LOG_FILE %log% 
FIND "ERROR 500: Error calling AB CSW node" %log%
SET Statut=%Statut%%ERRORLEVEL%

REM Third FME call, testing Alberta HTTP call, inducing an error to the second URL.  
set test_number=3
set source_1=met\source1.ffs
set source_2=met\source2.ffs
set source_3=met\source3.ffs
set source_4=met\source4.ffs
set resultat_1=met\resultat1.ffs
set resultat_2=met\resultat2.ffs
set resultat_3=met\resultat3.ffs
set resultat_4=met\resultat4.ffs
set log=met\log_%test_number%.log

IF EXIST %log% del %log%
IF EXIST %resultat_1% DEL %resultat_1%
IF EXIST %resultat_2% DEL %resultat_2%
IF EXIST %resultat_3% DEL %resultat_3%
IF EXIST %resultat_4% DEL %resultat_4%
%fme% met\metrique_ab_data_extraction.fmw ^
--CSW_QUERY_1 "https://geodiscover.alberta.ca/geoportal/csw?request=getRecords&service=CSW ..." ^
--CSW_QUERY_2 "http://httpstat.us/500" ^
--CSW_QUERY_3 "https://geodiscover.alberta.ca/geoportal/rest/metadata/item/a82d775c1dc841e4b0e61186531c0d8b/xml" ^
--ENTITY_SEARCH_LITERAL Alberta ^
--IN_FFS_FILE_1 %source_1% ^
--IN_FFS_FILE_2 %source_2% ^
--IN_FFS_FILE_3 %source_3% ^
--IN_FFS_FILE_4 %source_4% ^
--OUT_FFS_FILE_1 %resultat_1% ^
--OUT_FFS_FILE_2 %resultat_2% ^
--OUT_FFS_FILE_3 %resultat_3% ^
--OUT_FFS_FILE_4 %resultat_4% ^
--SAMPLE_SELECT Yes ^
--SAMPLE_SIZE 80 ^
--TIME_FILTER_DAYS 0 ^
--TIME_FILTER_MONTHS 24 ^
--TIME_STAMP 20200309 ^
--UNIT_TEST_HTTP_BYPASS No ^
--UNIT_TEST_PYCSW_BYPASS Yes ^
--LOG_FILE %log% 
FIND "ERROR 500: Unable to call CSW query" %log%
SET Statut=%Statut%%ERRORLEVEL%

REM Fourth FME call, testing Alberta HTTP call, inducing an error to the third URL.  
set test_number=4
set source_1=met\source1.ffs
set source_2=met\source2.ffs
set source_3=met\source3.ffs
set source_4=met\source4.ffs
set resultat_1=met\resultat1.ffs
set resultat_2=met\resultat2.ffs
set resultat_3=met\resultat3.ffs
set resultat_4=met\resultat4.ffs
set log=met\log_%test_number%.log

IF EXIST %log% del %log%
IF EXIST %resultat_1% DEL %resultat_1%
IF EXIST %resultat_2% DEL %resultat_2%
IF EXIST %resultat_3% DEL %resultat_3%
IF EXIST %resultat_4% DEL %resultat_4%
%fme% met\metrique_ab_data_extraction.fmw ^
--CSW_QUERY_1 "https://geodiscover.alberta.ca/geoportal/csw?request=getRecords&service=CSW ..." ^
--CSW_QUERY_2 "https://geodiscover.alberta.ca/geoportal/csw?request=getRecords&service=CSW&resultType=results&ElementSetName=summary&startPosition=1" ^
--CSW_QUERY_3 "http://httpstat.us/404" ^
--ENTITY_SEARCH_LITERAL Alberta ^
--IN_FFS_FILE_1 %source_1% ^
--IN_FFS_FILE_2 %source_2% ^
--IN_FFS_FILE_3 %source_3% ^
--IN_FFS_FILE_4 %source_4% ^
--OUT_FFS_FILE_1 %resultat_1% ^
--OUT_FFS_FILE_2 %resultat_2% ^
--OUT_FFS_FILE_3 %resultat_3% ^
--OUT_FFS_FILE_4 %resultat_4% ^
--SAMPLE_SELECT Yes ^
--SAMPLE_SIZE 80 ^
--TIME_FILTER_DAYS 0 ^
--TIME_FILTER_MONTHS 24 ^
--TIME_STAMP 20200309 ^
--UNIT_TEST_HTTP_BYPASS No ^
--UNIT_TEST_PYCSW_BYPASS Yes ^
--LOG_FILE %log% 
FIND "ERROR 404.  Unable to call" %log%
SET Statut=%Statut%%ERRORLEVEL%

REM Fifth FME call, bypassing HTTP Call and processing with FFS source data, with three FFS source files created following each HTTP call and acting as proxies for the HTTP results.
set test_number=5
SET etalon_1=met\etalon1.ffs
SET etalon_2=met\etalon2.ffs
SET etalon_3=met\etalon3.ffs
SET etalon_4=met\etalon4.ffs
set source_1=met\source1.ffs
set source_2=met\source2.ffs
set source_3=met\source3.ffs
set source_4=met\source4.ffs
set resultat_1=met\resultat1.ffs
set resultat_2=met\resultat2.ffs
set resultat_3=met\resultat3.ffs
set resultat_4=met\resultat4.ffs
set log=met\log_%test_number%.log
set log_comp_1=met\log_comp_%test_number%_1.log
set log_comp_2=met\log_comp_%test_number%_2.log
set log_comp_3=met\log_comp_%test_number%_3.log
set log_comp_4=met\log_comp_%test_number%_4.log

IF EXIST %log% del %log%
IF EXIST %resultat_1% DEL %resultat_1%
IF EXIST %resultat_2% DEL %resultat_2%
IF EXIST %resultat_3% DEL %resultat_3%
IF EXIST %resultat_4% DEL %resultat_4%
%fme% met\metrique_ab_data_extraction.fmw ^
--CSW_QUERY_1 "https://geodiscover.alberta.ca/geoportal/csw?request=getRecords&service=CSW ..." ^
--CSW_QUERY_2 "https://geodiscover.alberta.ca/geoportal/csw?request=getRecords&service=CSW&resultType=results&ElementSetName=summary&startPosition=1" ^
--CSW_QUERY_3 "https://geodiscover.alberta.ca/geoportal/rest/metadata/item/a82d775c1dc841e4b0e61186531c0d8b/xml" ^
--ENTITY_SEARCH_LITERAL Alberta ^
--IN_FFS_FILE_1 %source_1% ^
--IN_FFS_FILE_2 %source_2% ^
--IN_FFS_FILE_3 %source_3% ^
--IN_FFS_FILE_4 %source_4% ^
--OUT_FFS_FILE_1 %resultat_1% ^
--OUT_FFS_FILE_2 %resultat_2% ^
--OUT_FFS_FILE_3 %resultat_3% ^
--OUT_FFS_FILE_4 %resultat_4% ^
--SAMPLE_SELECT Yes ^
--SAMPLE_SIZE 80 ^
--TIME_FILTER_DAYS 0 ^
--TIME_FILTER_MONTHS 24 ^
--TIME_STAMP 20200309 ^
--UNIT_TEST_HTTP_BYPASS Yes ^
--UNIT_TEST_PYCSW_BYPASS Yes ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison data output with the standard.  Testing the output results prior to the second proxy HTTP call.
IF EXIST %log_comp_1% del %log_comp_1%
%fme% met\Comparateur.fmw ^
--IN_ETALON_FILE %etalon_1% ^
--IN_RESULTAT_FILE %resultat_1% ^
--LOG_FILE %log_comp_1% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison data output with the standard.  Testing output results prior to the third proxy HTTP call.
IF EXIST %log_comp_2% del %log_comp_2%
%fme% met\Comparateur.fmw ^
--IN_ETALON_FILE %etalon_2% ^
--IN_RESULTAT_FILE %resultat_2% ^
--LOG_FILE %log_comp_2% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison data output with the standard.  Testing output results after creation of XML deletion files.
IF EXIST %log_comp_3% del %log_comp_3%
%fme% met\Comparateur.fmw ^
--IN_ETALON_FILE %etalon_3% ^
--IN_RESULTAT_FILE %resultat_3% ^
--LOG_FILE %log_comp_3% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison data output with the standard.  Testing the final output results
IF EXIST %log_comp_4% del %log_comp_4%
%fme% met\Comparateur.fmw ^
--IN_ETALON_FILE %etalon_4% ^
--IN_RESULTAT_FILE %resultat_4% ^
--LOG_FILE %log_comp_4% 
SET Statut=%Statut%%ERRORLEVEL%

@IF [%Statut%] EQU [0000000000000] (
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


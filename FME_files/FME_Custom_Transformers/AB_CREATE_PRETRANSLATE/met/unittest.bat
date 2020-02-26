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
SET NomApp=AB_CREATE_PRETRANSLATE
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
set resultat_1=met\resultat_1.ffs
set resultat_2=met\resultat_2.ffs
set resultat_3=met\resultat_3.ffs
set log=met\log_%test_number%.log

IF EXIST %log% del %log%
%fme% met\metrique_ab_create_pretranslate.fmw ^
--CSW_QUERY_1 "https://geodiscover.alberta.ca/geoportal/csw?request=getRecords&service=CSW ..." ^
--CSW_QUERY_2 "https://geodiscover.alberta.ca/geoportal/csw?request=getRecords&service=CSW&resultType=results&ElementSetName=summary&startPosition=1" ^
--CSW_QUERY_3 "https://geodiscover.alberta.ca/geoportal/rest/metadata/item/a82d775c1dc841e4b0e61186531c0d8b/xml" ^
--IN_FFS_FILE_1 %source_1% ^
--IN_FFS_FILE_2 %source_2% ^
--IN_FFS_FILE_3 %source_3% ^
--OUT_FFS_FILE_1 %resultat_1% ^
--OUT_FFS_FILE_2 %resultat_2% ^
--OUT_FFS_FILE_3 %resultat_3% ^
--UNIT_TEST_HTTP_BYPASS No ^
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
set resultat_1=met\resultat_1.ffs
set resultat_2=met\resultat_2.ffs
set resultat_3=met\resultat_3.ffs
set log=met\log_%test_number%.log

IF EXIST %log% del %log%
%fme% met\metrique_ab_create_pretranslate.fmw ^
--CSW_QUERY_1 "http://httpstat.us/500" ^
--CSW_QUERY_2 "https://geodiscover.alberta.ca/geoportal/csw?request=getRecords&service=CSW&resultType=results&ElementSetName=summary&startPosition=1" ^
--CSW_QUERY_3 "https://geodiscover.alberta.ca/geoportal/rest/metadata/item/a82d775c1dc841e4b0e61186531c0d8b/xml" ^
--IN_FFS_FILE_1 %source_1% ^
--IN_FFS_FILE_2 %source_2% ^
--IN_FFS_FILE_3 %source_3% ^
--OUT_FFS_FILE_1 %resultat_1% ^
--OUT_FFS_FILE_2 %resultat_2% ^
--OUT_FFS_FILE_3 %resultat_3% ^
--UNIT_TEST_HTTP_BYPASS No ^
--LOG_FILE %log% 
FIND "ERROR 500: Error calling AB CSW node" %log%
SET Statut=%Statut%%ERRORLEVEL%

REM Third FME call, testing Alberta HTTP call, inducing an error to the second URL.  
set test_number=3
set source_1=met\source1.ffs
set source_2=met\source2.ffs
set source_3=met\source3.ffs
set resultat_1=met\resultat_1.ffs
set resultat_2=met\resultat_2.ffs
set resultat_3=met\resultat_3.ffs
set log=met\log_%test_number%.log

IF EXIST %log% del %log%
%fme% met\metrique_ab_create_pretranslate.fmw ^
--CSW_QUERY_1 "https://geodiscover.alberta.ca/geoportal/csw?request=getRecords&service=CSW ..." ^
--CSW_QUERY_2 "http://httpstat.us/500" ^
--CSW_QUERY_3 "https://geodiscover.alberta.ca/geoportal/rest/metadata/item/a82d775c1dc841e4b0e61186531c0d8b/xml" ^
--IN_FFS_FILE_1 %source_1% ^
--IN_FFS_FILE_2 %source_2% ^
--IN_FFS_FILE_3 %source_3% ^
--OUT_FFS_FILE_1 %resultat_1% ^
--OUT_FFS_FILE_2 %resultat_2% ^
--OUT_FFS_FILE_3 %resultat_3% ^
--UNIT_TEST_HTTP_BYPASS No ^
--LOG_FILE %log% 
FIND "ERROR 500: Unable to call CSW query" %log%
SET Statut=%Statut%%ERRORLEVEL%

REM Fourth FME call, testing Alberta HTTP call, inducing an error to the third URL.  
set test_number=3
set source_1=met\source1.ffs
set source_2=met\source2.ffs
set source_3=met\source3.ffs
set resultat_1=met\resultat_1.ffs
set resultat_2=met\resultat_2.ffs
set resultat_3=met\resultat_3.ffs
set log=met\log_%test_number%.log

IF EXIST %log% del %log%
%fme% met\metrique_ab_create_pretranslate.fmw ^
--CSW_QUERY_1 "https://geodiscover.alberta.ca/geoportal/csw?request=getRecords&service=CSW ..." ^
--CSW_QUERY_2 "https://geodiscover.alberta.ca/geoportal/csw?request=getRecords&service=CSW&resultType=results&ElementSetName=summary&startPosition=1" ^
--CSW_QUERY_3 "http://httpstat.us/404" ^
--IN_FFS_FILE_1 %source_1% ^
--IN_FFS_FILE_2 %source_2% ^
--IN_FFS_FILE_3 %source_3% ^
--OUT_FFS_FILE_1 %resultat_1% ^
--OUT_FFS_FILE_2 %resultat_2% ^
--OUT_FFS_FILE_3 %resultat_3% ^
--UNIT_TEST_HTTP_BYPASS No ^
--LOG_FILE %log% 
FIND "Unable to call: http://httpstat.us/404.  Error code 404" %log%
SET Statut=%Statut%%ERRORLEVEL%

@IF [%Statut%] EQU [00000000] (
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


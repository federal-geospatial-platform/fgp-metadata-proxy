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
SET NomApp=AWS_TRANSLATE_ENGLISH_TO_FRENCH
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


REM First FME call, with 12 compliant data records.  the first source file is input to preprocessing before the Python Caller and outputs an FFS resultat file before the Python caller for comparison with the first etalon file.  The second source file was produced using AWS Translate that is normally called in the Python caller on the FME Server.  A unit test enviromment cannot normally utilize AWS Translate so the Python Caller is bypassed and the second FFS file is inserted after the Python Caller to simulate the results of an actual AWS Translation.  The data from the second source file then is routed through the post AWS Translate transformers and the resultat file is output at the transformers regular output to compare with the etalon file.
set test_number=1
SET source_1=met\source1.ffs
SET source_2=met\source2.ffs
set etalon_1=met\etalon1.ffs
set etalon_2=met\etalon2.ffs
set resultat_1=met\resultat1.ffs
set resultat_2=met\resultat2.ffs
set log=met\log_%test_number%.log
set log_comp_1=met\log_comp_%test_number%_1.log
set log_comp_2=met\log_comp_%test_number%_2.log

IF EXIST %log% del %log%
IF EXIST met\resultat1.ffs DEL met\resultat1.ffs
IF EXIST met\resultat2.ffs DEL met\resultat2.ffs
%fme% met\metrique_aws_translate_english_to_french.fmw ^
--IN_FFS_FILE_1 %source_1% ^
--IN_FFS_FILE_2 %source_2% ^
--OUT_FFS_FILE_1 %resultat_1% ^
--OUT_FFS_FILE_2 %resultat_2% ^
--UNIT_TEST_AWS_BYPASS Yes ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison with the standard
IF EXIST %log_comp_1% del %log_comp_1%
%fme% met\Comparateur.fmw ^
--IN_ETALON_FILE %etalon_1% ^
--IN_RESULTAT_FILE %resultat_1% ^
--LOG_FILE %log_comp_1% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison with the standard
IF EXIST %log_comp_2% del %log_comp_2%
%fme% met\Comparateur.fmw ^
--IN_ETALON_FILE %etalon_2% ^
--IN_RESULTAT_FILE %resultat_2% ^
--LOG_FILE %log_comp_2% 
SET Statut=%Statut%%ERRORLEVEL%

@IF [%Statut%] EQU [00000] (
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


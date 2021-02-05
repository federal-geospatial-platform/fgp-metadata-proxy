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
SET NomApp=METADATA_VALUE_MAPPER
SET fme=%FME2019%


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

REM First FME call,creating FFS File with eleven compliant data records, mapping projection codespace values
SET test_number=1
SET source=met\source%test_number%.ffs
SET etalon=met\etalon%test_number%.ffs
SET lookup=met\CodespaceLookupUnitTest.csv
SET resultat=met\resultat.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log
SET att_to_map=spatialref{}.projection_system
SET code_refresh=NO
SET english_refresh=YES
SET error_not_mapped=NO
SET french_refresh=NO

IF EXIST %log% del %log%
IF EXIST met\resultat.ffs DEL met\resultat.ffs
%fme% met\metrique_metadata_value_mapper.fmw ^
--ATT_TO_MAP %att_to_map% ^
--CODE_REFRESH %code_refresh% ^
--ENGLISH_REFRESH %english_refresh% ^
--ERROR_NOT_MAPPED %error_not_mapped% ^
--FRENCH_REFRESH %french_refresh% ^
--IN_FFS_FILE %source% ^
--OUT_FFS_FILE %resultat% ^
--LOOKUP_TABLE %lookup% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison data output with the standard
IF EXIST %log_comp% del %log_comp%
%fme% met\Comparateur.fmw ^
--IN_ETALON_FILE %etalon% ^
--IN_RESULTAT_FILE %resultat% ^
--LOG_FILE %log_comp% 
SET Statut=%Statut%%ERRORLEVEL%

REM Second FME call, with eleven compliant data records, mapping country attribute values
SET test_number=2
SET source=met\source1.ffs
SET etalon=met\etalon%test_number%.ffs
SET lookup=met\CountryLookupUnitTest.csv
SET resultat=met\resultat.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log
SET att_to_map=contacts{}.country
SET code_refresh=NO
SET english_refresh=YES
SET error_not_mapped=NO
SET french_refresh=YES

IF EXIST %log% del %log%
IF EXIST met\resultat.ffs DEL met\resultat.ffs

%fme% met\metrique_metadata_value_mapper.fmw ^
--ATT_TO_MAP %att_to_map% ^
--CODE_REFRESH %code_refresh% ^
--ENGLISH_REFRESH %english_refresh% ^
--ERROR_NOT_MAPPED %error_not_mapped% ^
--FRENCH_REFRESH %french_refresh% ^
--IN_FFS_FILE %source% ^
--OUT_FFS_FILE %resultat% ^
--LOOKUP_TABLE %lookup% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison data output with the standard
IF EXIST %log_comp% del %log_comp%
%fme% met\Comparateur.fmw ^
--IN_ETALON_FILE %etalon% ^
--IN_RESULTAT_FILE %resultat% ^
--LOG_FILE %log_comp% 
SET Statut=%Statut%%ERRORLEVEL%

REM third FME call, with eleven compliant data records, mapping keyword attribute values
SET test_number=3
SET source=met\source1.ffs
SET etalon=met\etalon%test_number%.ffs
SET lookup=met\KeywordLookupUnitTest.csv
SET resultat=met\resultat.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log
SET att_to_map=iso_topic{}.topic_value
SET code_refresh=NO
SET english_refresh=YES
SET error_not_mapped=NO
SET french_refresh=NO

IF EXIST %log% del %log%
IF EXIST met\resultat.ffs DEL met\resultat.ffs

%fme% met\metrique_metadata_value_mapper.fmw ^
--ATT_TO_MAP %att_to_map% ^
--CODE_REFRESH %code_refresh% ^
--ENGLISH_REFRESH %english_refresh% ^
--ERROR_NOT_MAPPED %error_not_mapped% ^
--FRENCH_REFRESH %french_refresh% ^
--IN_FFS_FILE %source% ^
--OUT_FFS_FILE %resultat% ^
--LOOKUP_TABLE %lookup% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison data output with the standard
IF EXIST %log_comp% del %log_comp%
%fme% met\Comparateur.fmw ^
--IN_ETALON_FILE %etalon% ^
--IN_RESULTAT_FILE %resultat% ^
--LOG_FILE %log_comp% 
SET Statut=%Statut%%ERRORLEVEL%

REM fourth FME call, with eleven compliant data records, mapping progress attribute values
SET test_number=4
SET source=met\source1.ffs
SET etalon=met\etalon%test_number%.ffs
SET lookup=met\ProgressLookupUnitTest.csv
SET resultat=met\resultat.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log
SET att_to_map=progress_code
SET code_refresh=YES
SET english_refresh=YES
SET error_not_mapped=YES
SET french_refresh=YES

IF EXIST %log% del %log%
IF EXIST met\resultat.ffs DEL met\resultat.ffs

%fme% met\metrique_metadata_value_mapper.fmw ^
--ATT_TO_MAP %att_to_map% ^
--CODE_REFRESH %code_refresh% ^
--ENGLISH_REFRESH %english_refresh% ^
--ERROR_NOT_MAPPED %error_not_mapped% ^
--FRENCH_REFRESH %french_refresh% ^
--IN_FFS_FILE %source% ^
--OUT_FFS_FILE %resultat% ^
--LOOKUP_TABLE %lookup% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison data output with the standard
IF EXIST %log_comp% del %log_comp%
%fme% met\Comparateur.fmw ^
--IN_ETALON_FILE %etalon% ^
--IN_RESULTAT_FILE %resultat% ^
--LOG_FILE %log_comp% 
SET Statut=%Statut%%ERRORLEVEL%

REM fifth FME call, mapping progress attribute values with ten compliant data records, and one with that will create mapping error
SET test_number=5
SET source=met\source2.ffs
SET etalon=met\etalon%test_number%.ffs
SET lookup=met\ProgressLookupUnitTest.csv
SET resultat=met\resultat.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log
SET att_to_map=progress_code
SET code_refresh=YES
SET english_refresh=YES
SET error_not_mapped=YES
SET french_refresh=YES

IF EXIST %log% del %log%
IF EXIST met\resultat.ffs DEL met\resultat.ffs

%fme% met\metrique_metadata_value_mapper.fmw ^
--ATT_TO_MAP %att_to_map% ^
--CODE_REFRESH %code_refresh% ^
--ENGLISH_REFRESH %english_refresh% ^
--ERROR_NOT_MAPPED %error_not_mapped% ^
--FRENCH_REFRESH %french_refresh% ^
--IN_FFS_FILE %source% ^
--OUT_FFS_FILE %resultat% ^
--LOOKUP_TABLE %lookup% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison data output with the standard
IF EXIST %log_comp% del %log_comp%
%fme% met\Comparateur.fmw ^
--IN_ETALON_FILE %etalon% ^
--IN_RESULTAT_FILE %resultat% ^
--LOG_FILE %log_comp% 
SET Statut=%Statut%%ERRORLEVEL%

REM sixth FME call, mapping projection attribute values with ten compliant data records
SET test_number=6
SET source=met\source1.ffs
SET etalon=met\etalon%test_number%.ffs
SET lookup=met\ProjectionLookupUnitTest.csv
SET resultat=met\resultat.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log
SET att_to_map=spatialref{}.projection_name
SET code_refresh=NO
SET english_refresh=YES
SET error_not_mapped=NO
SET french_refresh=NO

IF EXIST %log% del %log%
IF EXIST met\resultat.ffs DEL met\resultat.ffs

%fme% met\metrique_metadata_value_mapper.fmw ^
--ATT_TO_MAP %att_to_map% ^
--CODE_REFRESH %code_refresh% ^
--ENGLISH_REFRESH %english_refresh% ^
--ERROR_NOT_MAPPED %error_not_mapped% ^
--FRENCH_REFRESH %french_refresh% ^
--IN_FFS_FILE %source% ^
--OUT_FFS_FILE %resultat% ^
--LOOKUP_TABLE %lookup% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison data output with the standard
IF EXIST %log_comp% del %log_comp%
%fme% met\Comparateur.fmw ^
--IN_ETALON_FILE %etalon% ^
--IN_RESULTAT_FILE %resultat% ^
--LOG_FILE %log_comp% 
SET Statut=%Statut%%ERRORLEVEL%

REM seventh FME call, mapping spatial type attribute values with ten compliant data records
SET test_number=7
SET source=met\source1.ffs
SET etalon=met\etalon%test_number%.ffs
SET lookup=met\SpatialRepLookupUnitTest.csv
SET resultat=met\resultat.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log
SET att_to_map=spatial_representation_type
SET code_refresh=YES
SET english_refresh=YES
SET error_not_mapped=YES
SET french_refresh=YES

IF EXIST %log% del %log%
IF EXIST met\resultat.ffs DEL met\resultat.ffs

%fme% met\metrique_metadata_value_mapper.fmw ^
--ATT_TO_MAP %att_to_map% ^
--CODE_REFRESH %code_refresh% ^
--ENGLISH_REFRESH %english_refresh% ^
--ERROR_NOT_MAPPED %error_not_mapped% ^
--FRENCH_REFRESH %french_refresh% ^
--IN_FFS_FILE %source% ^
--OUT_FFS_FILE %resultat% ^
--LOOKUP_TABLE %lookup% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison data output with the standard
IF EXIST %log_comp% del %log_comp%
%fme% met\Comparateur.fmw ^
--IN_ETALON_FILE %etalon% ^
--IN_RESULTAT_FILE %resultat% ^
--LOG_FILE %log_comp% 
SET Statut=%Statut%%ERRORLEVEL%

REM eighth FME call, mapping spatial type attribute values with nine compliant data records, and one that produces error
SET test_number=8
SET source=met\source2.ffs
SET etalon=met\etalon%test_number%.ffs
SET lookup=met\SpatialRepLookupUnitTest.csv
SET resultat=met\resultat.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log
SET att_to_map=spatial_representation_type
SET code_refresh=YES
SET english_refresh=YES
SET error_not_mapped=YES
SET french_refresh=YES

IF EXIST %log% del %log%
IF EXIST met\resultat.ffs DEL met\resultat.ffs

%fme% met\metrique_metadata_value_mapper.fmw ^
--ATT_TO_MAP %att_to_map% ^
--CODE_REFRESH %code_refresh% ^
--ENGLISH_REFRESH %english_refresh% ^
--ERROR_NOT_MAPPED %error_not_mapped% ^
--FRENCH_REFRESH %french_refresh% ^
--IN_FFS_FILE %source% ^
--OUT_FFS_FILE %resultat% ^
--LOOKUP_TABLE %lookup% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison data output with the standard
IF EXIST %log_comp% del %log_comp%
%fme% met\Comparateur.fmw ^
--IN_ETALON_FILE %etalon% ^
--IN_RESULTAT_FILE %resultat% ^
--LOG_FILE %log_comp% 
SET Statut=%Statut%%ERRORLEVEL%

REM ninth FME call, mapping GIS terms used as resources names and reversing french translation errors ie: REST translated to RESTEZ-TOI and SHP translated to CHUT.  Source file has two data records with each of these errors.

SET test_number=9
SET source=met\source2.ffs
SET etalon=met\etalon%test_number%.ffs
SET lookup=met\TranslationLookupUnitTest.csv
SET resultat=met\resultat.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log
SET att_to_map=resources{}.name
SET code_refresh=NO
SET english_refresh=NO
SET error_not_mapped=NO
SET french_refresh=YES

IF EXIST %log% del %log%
IF EXIST met\resultat.ffs DEL met\resultat.ffs

%fme% met\metrique_metadata_value_mapper.fmw ^
--ATT_TO_MAP %att_to_map% ^
--CODE_REFRESH %code_refresh% ^
--ENGLISH_REFRESH %english_refresh% ^
--ERROR_NOT_MAPPED %error_not_mapped% ^
--FRENCH_REFRESH %french_refresh% ^
--IN_FFS_FILE %source% ^
--OUT_FFS_FILE %resultat% ^
--LOOKUP_TABLE %lookup% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison data output with the standard
IF EXIST %log_comp% del %log_comp%
%fme% met\Comparateur.fmw ^
--IN_ETALON_FILE %etalon% ^
--IN_RESULTAT_FILE %resultat% ^
--LOG_FILE %log_comp% 
SET Statut=%Statut%%ERRORLEVEL%

REM tenth FME call, mapping update cycle attribute values with ten compliant data records

SET test_number=10
SET source=met\source1.ffs
SET etalon=met\etalon%test_number%.ffs
SET lookup=met\UpdateLookupUnitTest.csv
SET resultat=met\resultat.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log
SET att_to_map=resource_update_cycle
SET code_refresh=YES
SET english_refresh=YES
SET error_not_mapped=YES
SET french_refresh=YES

IF EXIST %log% del %log%
IF EXIST met\resultat.ffs DEL met\resultat.ffs

%fme% met\metrique_metadata_value_mapper.fmw ^
--ATT_TO_MAP %att_to_map% ^
--CODE_REFRESH %code_refresh% ^
--ENGLISH_REFRESH %english_refresh% ^
--ERROR_NOT_MAPPED %error_not_mapped% ^
--FRENCH_REFRESH %french_refresh% ^
--IN_FFS_FILE %source% ^
--OUT_FFS_FILE %resultat% ^
--LOOKUP_TABLE %lookup% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison data output with the standard
IF EXIST %log_comp% del %log_comp%
%fme% met\Comparateur.fmw ^
--IN_ETALON_FILE %etalon% ^
--IN_RESULTAT_FILE %resultat% ^
--LOG_FILE %log_comp% 
SET Statut=%Statut%%ERRORLEVEL%

REM eleventh FME call, mapping update cycle attribute values with nine compliant data records, and one with a mapping error

SET test_number=11
SET source=met\source2.ffs
SET etalon=met\etalon%test_number%.ffs
SET lookup=met\UpdateLookupUnitTest.csv
SET resultat=met\resultat.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log
SET att_to_map=resource_update_cycle
SET code_refresh=YES
SET english_refresh=YES
SET error_not_mapped=YES
SET french_refresh=YES

IF EXIST %log% del %log%
IF EXIST met\resultat.ffs DEL met\resultat.ffs

%fme% met\metrique_metadata_value_mapper.fmw ^
--ATT_TO_MAP %att_to_map% ^
--CODE_REFRESH %code_refresh% ^
--ENGLISH_REFRESH %english_refresh% ^
--ERROR_NOT_MAPPED %error_not_mapped% ^
--FRENCH_REFRESH %french_refresh% ^
--IN_FFS_FILE %source% ^
--OUT_FFS_FILE %resultat% ^
--LOOKUP_TABLE %lookup% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison data output with the standard
IF EXIST %log_comp% del %log_comp%
%fme% met\Comparateur.fmw ^
--IN_ETALON_FILE %etalon% ^
--IN_RESULTAT_FILE %resultat% ^
--LOG_FILE %log_comp% 
SET Statut=%Statut%%ERRORLEVEL%

REM twelfth FME call, mapping role attribute values with ten compliant data records

SET test_number=12
SET source=met\source1.ffs
SET etalon=met\etalon%test_number%.ffs
SET lookup=met\RoleLookupUnitTest.csv
SET resultat=met\resultat.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log
SET att_to_map=contacts{}.role
SET code_refresh=YES
SET english_refresh=YES
SET error_not_mapped=YES
SET french_refresh=YES

IF EXIST %log% del %log%
IF EXIST met\resultat.ffs DEL met\resultat.ffs

%fme% met\metrique_metadata_value_mapper.fmw ^
--ATT_TO_MAP %att_to_map% ^
--CODE_REFRESH %code_refresh% ^
--ENGLISH_REFRESH %english_refresh% ^
--ERROR_NOT_MAPPED %error_not_mapped% ^
--FRENCH_REFRESH %french_refresh% ^
--IN_FFS_FILE %source% ^
--OUT_FFS_FILE %resultat% ^
--LOOKUP_TABLE %lookup% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison data output with the standard
IF EXIST %log_comp% del %log_comp%
%fme% met\Comparateur.fmw ^
--IN_ETALON_FILE %etalon% ^
--IN_RESULTAT_FILE %resultat% ^
--LOG_FILE %log_comp% 
SET Statut=%Statut%%ERRORLEVEL%

REM thirteenth FME call, mapping role attribute values with nine compliant data records, and one with a mapping error

SET test_number=13
SET source=met\source2.ffs
SET etalon=met\etalon%test_number%.ffs
SET lookup=met\RoleLookupUnitTest.csv
SET resultat=met\resultat.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log
SET att_to_map=contacts{}.role
SET code_refresh=YES
SET english_refresh=YES
SET error_not_mapped=YES
SET french_refresh=YES

IF EXIST %log% del %log%
IF EXIST met\resultat.ffs DEL met\resultat.ffs

%fme% met\metrique_metadata_value_mapper.fmw ^
--ATT_TO_MAP %att_to_map% ^
--CODE_REFRESH %code_refresh% ^
--ENGLISH_REFRESH %english_refresh% ^
--ERROR_NOT_MAPPED %error_not_mapped% ^
--FRENCH_REFRESH %french_refresh% ^
--IN_FFS_FILE %source% ^
--OUT_FFS_FILE %resultat% ^
--LOOKUP_TABLE %lookup% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison data output with the standard
IF EXIST %log_comp% del %log_comp%
%fme% met\Comparateur.fmw ^
--IN_ETALON_FILE %etalon% ^
--IN_RESULTAT_FILE %resultat% ^
--LOG_FILE %log_comp% 
SET Statut=%Statut%%ERRORLEVEL%

@IF [%Statut%] EQU [0000000000000000000000000000] (
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


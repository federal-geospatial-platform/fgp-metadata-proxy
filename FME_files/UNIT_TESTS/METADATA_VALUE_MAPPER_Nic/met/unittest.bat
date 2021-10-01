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
REM On test le mapping sur le progress code, refresh code/eng/fr
SET test_number=1
SET etalon=met\etalon_%test_number%.ffs
SET lookup=met\lookuptables\progress_code.csv
SET resultat=met\resultat_%test_number%.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log
SET att_to_map=progress_code
SET code_refresh=YES
SET english_refresh=YES
SET error_not_mapped=NO
SET french_refresh=YES

IF EXIST %log% del %log%
IF EXIST %resultat% DEL %resultat%
%fme% met\metrique_metadata_value_mapper.fmw ^
--ATT_TO_MAP %att_to_map% ^
--CODE_REFRESH %code_refresh% ^
--ENGLISH_REFRESH %english_refresh% ^
--ERROR_NOT_MAPPED %error_not_mapped% ^
--FRENCH_REFRESH %french_refresh% ^
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
REM On test le mapping sur le contact{}.role, refresh code/eng/fr
REM ============================================================================
SET test_number=2
SET etalon=met\etalon_%test_number%.ffs
SET lookup=met\lookuptables\role.csv
SET resultat=met\resultat_%test_number%.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log
SET att_to_map=contact{}.role
SET code_refresh=YES
SET english_refresh=YES
SET error_not_mapped=NO
SET french_refresh=YES

IF EXIST %log% del %log%
IF EXIST %resultat% DEL %resultat%
%fme% met\metrique_metadata_value_mapper.fmw ^
--ATT_TO_MAP %att_to_map% ^
--CODE_REFRESH %code_refresh% ^
--ENGLISH_REFRESH %english_refresh% ^
--ERROR_NOT_MAPPED %error_not_mapped% ^
--FRENCH_REFRESH %french_refresh% ^
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
REM ========================== TEST  #3   ======================================
REM ============================================================================
REM On test le mapping sur le progress_code, pas de refresh anglais et francais, uniquement le code
REM ============================================================================
SET test_number=3
SET etalon=met\etalon_%test_number%.ffs
SET lookup=met\lookuptables\progress_code.csv
SET resultat=met\resultat_%test_number%.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log
SET att_to_map=progress_code
SET code_refresh=YES
SET english_refresh=NO
SET error_not_mapped=NO
SET french_refresh=NO

IF EXIST %log% del %log%
IF EXIST %resultat% DEL %resultat%
%fme% met\metrique_metadata_value_mapper.fmw ^
--ATT_TO_MAP %att_to_map% ^
--CODE_REFRESH %code_refresh% ^
--ENGLISH_REFRESH %english_refresh% ^
--ERROR_NOT_MAPPED %error_not_mapped% ^
--FRENCH_REFRESH %french_refresh% ^
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
REM ========================== TEST  #4   ======================================
REM ============================================================================
REM On test le mapping sur le role, pas de refresh anglais et francais, uniquement le code
REM ============================================================================
SET test_number=4
SET etalon=met\etalon_%test_number%.ffs
SET lookup=met\lookuptables\role.csv
SET resultat=met\resultat_%test_number%.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log
SET att_to_map=contact{}.role
SET code_refresh=YES
SET english_refresh=NO
SET error_not_mapped=NO
SET french_refresh=NO

IF EXIST %log% del %log%
IF EXIST %resultat% DEL %resultat%
%fme% met\metrique_metadata_value_mapper.fmw ^
--ATT_TO_MAP %att_to_map% ^
--CODE_REFRESH %code_refresh% ^
--ENGLISH_REFRESH %english_refresh% ^
--ERROR_NOT_MAPPED %error_not_mapped% ^
--FRENCH_REFRESH %french_refresh% ^
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
REM ========================== TEST  #5   ======================================
REM ============================================================================
REM On test le mapping sur le progress_code, pas de refresh anglais et code, uniquement le français
REM ============================================================================
SET test_number=5
SET etalon=met\etalon_%test_number%.ffs
SET lookup=met\lookuptables\progress_code.csv
SET resultat=met\resultat_%test_number%.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log
SET att_to_map=progress_code
SET code_refresh=NO
SET english_refresh=NO
SET error_not_mapped=NO
SET french_refresh=YES

IF EXIST %log% del %log%
IF EXIST %resultat% DEL %resultat%
%fme% met\metrique_metadata_value_mapper.fmw ^
--ATT_TO_MAP %att_to_map% ^
--CODE_REFRESH %code_refresh% ^
--ENGLISH_REFRESH %english_refresh% ^
--ERROR_NOT_MAPPED %error_not_mapped% ^
--FRENCH_REFRESH %french_refresh% ^
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
REM ========================== TEST  #6   ======================================
REM ============================================================================
REM On test le mapping sur le role, pas de refresh anglais et code, uniquement le français
REM ============================================================================
SET test_number=6
SET etalon=met\etalon_%test_number%.ffs
SET lookup=met\lookuptables\role.csv
SET resultat=met\resultat_%test_number%.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log
SET att_to_map=contact{}.role
SET code_refresh=NO
SET english_refresh=NO
SET error_not_mapped=NO
SET french_refresh=YES

IF EXIST %log% del %log%
IF EXIST %resultat% DEL %resultat%
%fme% met\metrique_metadata_value_mapper.fmw ^
--ATT_TO_MAP %att_to_map% ^
--CODE_REFRESH %code_refresh% ^
--ENGLISH_REFRESH %english_refresh% ^
--ERROR_NOT_MAPPED %error_not_mapped% ^
--FRENCH_REFRESH %french_refresh% ^
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
REM ========================== TEST  #7   ======================================
REM ============================================================================
REM On test le mapping sur le progress_code, uniquement refresh en
REM ============================================================================
SET test_number=7
SET etalon=met\etalon_%test_number%.ffs
SET lookup=met\lookuptables\progress_code.csv
SET resultat=met\resultat_%test_number%.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log
SET att_to_map=progress_code
SET code_refresh=NO
SET english_refresh=YES
SET error_not_mapped=NO
SET french_refresh=NO

IF EXIST %log% del %log%
IF EXIST %resultat% DEL %resultat%
%fme% met\metrique_metadata_value_mapper.fmw ^
--ATT_TO_MAP %att_to_map% ^
--CODE_REFRESH %code_refresh% ^
--ENGLISH_REFRESH %english_refresh% ^
--ERROR_NOT_MAPPED %error_not_mapped% ^
--FRENCH_REFRESH %french_refresh% ^
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
REM ========================== TEST  #8   ======================================
REM ============================================================================
REM On test le mapping sur le role, uniquement refresh en
REM ============================================================================
SET test_number=8
SET etalon=met\etalon_%test_number%.ffs
SET lookup=met\lookuptables\role.csv
SET resultat=met\resultat_%test_number%.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log
SET att_to_map=contact{}.role
SET code_refresh=NO
SET english_refresh=YES
SET error_not_mapped=NO
SET french_refresh=NO

IF EXIST %log% del %log%
IF EXIST %resultat% DEL %resultat%
%fme% met\metrique_metadata_value_mapper.fmw ^
--ATT_TO_MAP %att_to_map% ^
--CODE_REFRESH %code_refresh% ^
--ENGLISH_REFRESH %english_refresh% ^
--ERROR_NOT_MAPPED %error_not_mapped% ^
--FRENCH_REFRESH %french_refresh% ^
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
REM ========================== TEST  #9A   ======================================
REM ============================================================================
REM On test le mapping sur le progress_code mais avec une mauvaise lookup table
REM On n'active pas la switch pour logger les erreurs 
REM Les switch refresh sont sans impact
REM ============================================================================
SET test_number=9A
SET etalon=met\etalon_%test_number%.ffs
SET lookup=met\lookuptables\role.csv
SET resultat=met\resultat_%test_number%.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log
SET att_to_map=progress_code
SET code_refresh=NO
SET english_refresh=YES
SET error_not_mapped=NO
SET french_refresh=NO

IF EXIST %log% del %log%
IF EXIST %resultat% DEL %resultat%
%fme% met\metrique_metadata_value_mapper.fmw ^
--ATT_TO_MAP %att_to_map% ^
--CODE_REFRESH %code_refresh% ^
--ENGLISH_REFRESH %english_refresh% ^
--ERROR_NOT_MAPPED %error_not_mapped% ^
--FRENCH_REFRESH %french_refresh% ^
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
REM ========================== TEST  #9B   ======================================
REM ============================================================================
REM On test le mapping sur le progress_code mais avec une mauvaise lookup table
REM On active la switch pour logger les erreurs 
REM Les switch refresh sont sans impact
REM ============================================================================
SET test_number=9B
SET etalon=met\etalon_%test_number%.ffs
SET lookup=met\lookuptables\role.csv
SET resultat=met\resultat_%test_number%.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log
SET att_to_map=progress_code
SET code_refresh=NO
SET english_refresh=YES
SET error_not_mapped=YES
SET french_refresh=NO

IF EXIST %log% del %log%
IF EXIST %resultat% DEL %resultat%
%fme% met\metrique_metadata_value_mapper.fmw ^
--ATT_TO_MAP %att_to_map% ^
--CODE_REFRESH %code_refresh% ^
--ENGLISH_REFRESH %english_refresh% ^
--ERROR_NOT_MAPPED %error_not_mapped% ^
--FRENCH_REFRESH %french_refresh% ^
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
REM ========================== TEST  #10A   ======================================
REM ============================================================================
REM On test le mapping sur le role mais avec une mauvaise lookup table
REM On n'active pas la switch pour logger les erreurs 
REM Les switch refresh sont sans impact
REM ============================================================================
SET test_number=10A
SET etalon=met\etalon_%test_number%.ffs
SET lookup=met\lookuptables\progress_code.csv
SET resultat=met\resultat_%test_number%.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log
SET att_to_map=contact{}.role
SET code_refresh=NO
SET english_refresh=YES
SET error_not_mapped=NO
SET french_refresh=NO

IF EXIST %log% del %log%
IF EXIST %resultat% DEL %resultat%
%fme% met\metrique_metadata_value_mapper.fmw ^
--ATT_TO_MAP %att_to_map% ^
--CODE_REFRESH %code_refresh% ^
--ENGLISH_REFRESH %english_refresh% ^
--ERROR_NOT_MAPPED %error_not_mapped% ^
--FRENCH_REFRESH %french_refresh% ^
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
REM ========================== TEST  #10B   ======================================
REM ============================================================================
REM On test le mapping sur le role mais avec une mauvaise lookup table
REM On active la switch pour logger les erreurs 
REM Les switch refresh sont sans impact
REM ============================================================================
SET test_number=10B
SET etalon=met\etalon_%test_number%.ffs
SET lookup=met\lookuptables\progress_code.csv
SET resultat=met\resultat_%test_number%.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log
SET att_to_map=contact{}.role
SET code_refresh=NO
SET english_refresh=YES
SET error_not_mapped=YES
SET french_refresh=NO

IF EXIST %log% del %log%
IF EXIST %resultat% DEL %resultat%
%fme% met\metrique_metadata_value_mapper.fmw ^
--ATT_TO_MAP %att_to_map% ^
--CODE_REFRESH %code_refresh% ^
--ENGLISH_REFRESH %english_refresh% ^
--ERROR_NOT_MAPPED %error_not_mapped% ^
--FRENCH_REFRESH %french_refresh% ^
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
REM ========================== TEST  #11   ======================================
REM ============================================================================
REM On test l'accumulation d'erreur lors du mapping
REM On utilise une source manuel contenant deja des erreurs de mapping
REM On active la switch pour logger les erreurs 
REM Les switch refresh sont sans impact
REM ============================================================================

SET test_number=11
SET etalon=met\etalon_%test_number%.ffs
SET lookup=met\lookuptables\progress_code.csv
SET resultat=met\resultat_%test_number%.ffs
set source=met\source_%test_number%.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log
SET att_to_map=contact{}.role
SET code_refresh=NO
SET english_refresh=YES
SET error_not_mapped=YES
SET french_refresh=NO

IF EXIST %log% del %log%
IF EXIST %resultat% DEL %resultat%
%fme% met\metrique_metadata_value_mapper.fmw ^
--ATT_TO_MAP %att_to_map% ^
--CODE_REFRESH %code_refresh% ^
--ENGLISH_REFRESH %english_refresh% ^
--ERROR_NOT_MAPPED %error_not_mapped% ^
--FRENCH_REFRESH %french_refresh% ^
--OUT_FFS_FILE %resultat% ^
--LOOKUP_TABLE %lookup% ^
--IN_FFS_MANUAL_SOURCE %source% ^
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
REM ========================== TEST  #ERREUR-1  ================================
REM ============================================================================
REM On test une lookup table sans attribut original_value
REM ============================================================================

SET test_number=ERREUR-1
SET etalon=met\etalon_%test_number%.ffs
SET lookup=met\lookuptables\%test_number%.csv
SET resultat=met\resultat_%test_number%.ffs
set source=met\source_%test_number%.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log
SET att_to_map=contact{}.role
SET code_refresh=NO
SET english_refresh=YES
SET error_not_mapped=YES
SET french_refresh=NO

IF EXIST %log% del %log%
IF EXIST %resultat% DEL %resultat%
%fme% met\metrique_metadata_value_mapper.fmw ^
--ATT_TO_MAP %att_to_map% ^
--CODE_REFRESH %code_refresh% ^
--ENGLISH_REFRESH %english_refresh% ^
--ERROR_NOT_MAPPED %error_not_mapped% ^
--FRENCH_REFRESH %french_refresh% ^
--OUT_FFS_FILE %resultat% ^
--LOOKUP_TABLE %lookup% ^
--LOG_FILE %log% 

FIND "ERROR: No value for original_value in look-up table" %log%
SET Statut=%Statut%%ERRORLEVEL%





REM ============================================================================
REM ========================== TEST  #ERREUR-2  ================================
REM ============================================================================
REM On test une lookup table sans attribut real_value_english
REM ============================================================================

SET test_number=ERREUR-2
SET etalon=met\etalon_%test_number%.ffs
SET lookup=met\lookuptables\%test_number%.csv
SET resultat=met\resultat_%test_number%.ffs
set source=met\source_%test_number%.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log
SET att_to_map=contact{}.role
SET code_refresh=NO
SET english_refresh=YES
SET error_not_mapped=YES
SET french_refresh=NO

IF EXIST %log% del %log%
IF EXIST %resultat% DEL %resultat%
%fme% met\metrique_metadata_value_mapper.fmw ^
--ATT_TO_MAP %att_to_map% ^
--CODE_REFRESH %code_refresh% ^
--ENGLISH_REFRESH %english_refresh% ^
--ERROR_NOT_MAPPED %error_not_mapped% ^
--FRENCH_REFRESH %french_refresh% ^
--OUT_FFS_FILE %resultat% ^
--LOOKUP_TABLE %lookup% ^
--LOG_FILE %log% 

FIND "ERROR: No value for real_value_english in look-up table" %log%
SET Statut=%Statut%%ERRORLEVEL%

REM ON refait le même test avec ERROR_NOT_MAPPED à NO.
REM On vérifie uniquement que je programme fonctionne, le fonctionnement a déjà été vérifié par d'autre tests.
IF EXIST %log% del %log%
IF EXIST %resultat% DEL %resultat%
%fme% met\metrique_metadata_value_mapper.fmw ^
--ATT_TO_MAP %att_to_map% ^
--CODE_REFRESH %code_refresh% ^
--ENGLISH_REFRESH %english_refresh% ^
--ERROR_NOT_MAPPED NO ^
--FRENCH_REFRESH %french_refresh% ^
--OUT_FFS_FILE %resultat% ^
--LOOKUP_TABLE %lookup% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%



REM ============================================================================
REM ========================== TEST  #ERREUR-3  ================================
REM ============================================================================
REM On test une lookup table sans attribut real_value_french
REM ============================================================================

SET test_number=ERREUR-3
SET etalon=met\etalon_%test_number%.ffs
SET lookup=met\lookuptables\%test_number%.csv
SET resultat=met\resultat_%test_number%.ffs
set source=met\source_%test_number%.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log
SET att_to_map=contact{}.role
SET code_refresh=NO
SET english_refresh=NO
SET error_not_mapped=YES
SET french_refresh=YES

IF EXIST %log% del %log%
IF EXIST %resultat% DEL %resultat%
%fme% met\metrique_metadata_value_mapper.fmw ^
--ATT_TO_MAP %att_to_map% ^
--CODE_REFRESH %code_refresh% ^
--ENGLISH_REFRESH %english_refresh% ^
--ERROR_NOT_MAPPED %error_not_mapped% ^
--FRENCH_REFRESH %french_refresh% ^
--OUT_FFS_FILE %resultat% ^
--LOOKUP_TABLE %lookup% ^
--LOG_FILE %log% 

FIND "ERROR: No value for real_value_french in look-up table" %log%
SET Statut=%Statut%%ERRORLEVEL%

REM ON refait le même test avec ERROR_NOT_MAPPED à NO.
REM On vérifie uniquement que je programme fonctionne, le fonctionnement a déjà été vérifié par d'autre tests.
IF EXIST %log% del %log%
IF EXIST %resultat% DEL %resultat%
%fme% met\metrique_metadata_value_mapper.fmw ^
--ATT_TO_MAP %att_to_map% ^
--CODE_REFRESH %code_refresh% ^
--ENGLISH_REFRESH %english_refresh% ^
--ERROR_NOT_MAPPED NO ^
--FRENCH_REFRESH %french_refresh% ^
--OUT_FFS_FILE %resultat% ^
--LOOKUP_TABLE %lookup% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%

REM ============================================================================
REM ========================== TEST  #ERREUR-4  ================================
REM ============================================================================
REM On test une lookup table sans attribut real_value_french
REM ============================================================================

SET test_number=ERREUR-4
SET etalon=met\etalon_%test_number%.ffs
SET lookup=met\lookuptables\%test_number%.csv
SET resultat=met\resultat_%test_number%.ffs
set source=met\source_%test_number%.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log
SET att_to_map=contact{}.role
SET code_refresh=YES
SET english_refresh=NO
SET error_not_mapped=YES
SET french_refresh=NO

IF EXIST %log% del %log%
IF EXIST %resultat% DEL %resultat%
%fme% met\metrique_metadata_value_mapper.fmw ^
--ATT_TO_MAP %att_to_map% ^
--CODE_REFRESH %code_refresh% ^
--ENGLISH_REFRESH %english_refresh% ^
--ERROR_NOT_MAPPED %error_not_mapped% ^
--FRENCH_REFRESH %french_refresh% ^
--OUT_FFS_FILE %resultat% ^
--LOOKUP_TABLE %lookup% ^
--LOG_FILE %log% 

FIND "ERROR: No value for code_value in look-up table" %log%
SET Statut=%Statut%%ERRORLEVEL%

REM ON refait le même test avec ERROR_NOT_MAPPED à NO.
REM On vérifie uniquement que je programme fonctionne, le fonctionnement a déjà été vérifié par d'autre tests.
IF EXIST %log% del %log%
IF EXIST %resultat% DEL %resultat%
%fme% met\metrique_metadata_value_mapper.fmw ^
--ATT_TO_MAP %att_to_map% ^
--CODE_REFRESH %code_refresh% ^
--ENGLISH_REFRESH %english_refresh% ^
--ERROR_NOT_MAPPED NO ^
--FRENCH_REFRESH %french_refresh% ^
--OUT_FFS_FILE %resultat% ^
--LOOKUP_TABLE %lookup% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%



@IF [%Statut%] EQU [00000000000000000000000000000000000] (
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


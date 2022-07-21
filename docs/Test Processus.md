# Tests de processus dans FME

- [Mise en contexte](#Mise-en-contexte)
- [Le fichier de commandes](#Le-fichier-de-commandes)
- [Pré-conditions aux tests de processus](#Pré-conditions-aux-tests-de-processus)
- [Mise en place des répertoires](#Mise-en-place-des-répertoires)
- [Exécution du test de processus](#Exécution-du-test-de-processus)

## Mise en contexte

Les tests de processus sont complémentaires aux [tests unitaires](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/blob/master/docs/Tests%20Unitaires.md).  Ils servent à vérifier si un _Workbench FME_ fonctionne correctement pour une province ou un territoire donnée.  Les tests de processus n'ont pas pour but de tester tous les états, cas ou erreurs possibles qu'un _Workbench FME_ peut prendre car ceci reviendrait à dupliquer en grande partie les tests unitaires qui sont déjà faits pour les différents _Custom Transformers_.  Les tests de processus sont donc simples mais ils permettent de vérifier le bon fonctionnement global d'un _Workbench FME_ pour un sous-ensemble de métadonnées.

## Le fichier de commandes

Le fichiers de commandes pour les tests de processus est similaires aux fichiers de commandes DOS utilisés pour les [tests unitaires](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/blob/master/docs/Tests%20Unitaires.md). Le test de processus se trouve dans le répertoires ...\fgp-metadata-proxy\FME_files\UNIT_TESTS\PT_HARVESTER. Il n'y qu'un seul répertoire de tests de processus et il est bon pour tous les PT ce qui permet de de normaliser les test et de faciliter la maintenance des tests de processus.

## Pré-conditions aux tests de processus

Voici quelques éléments obligatoires qui doivent être faits avant de pouvoir intégrer un _Workbench FME_ dans le test de processus normalisés:

  - Le nom du _Workbench FME_ doit être sous la forme xx_PROD.fmw où xx est le code de province à deux lettres (ex.: NB_PROD.fmw)
  - Le _Workbench FME_ doit contenir les Writer et les paramètres suivants:
    - XML_PASSED lié au Private Parameter OUT_XML_PASSED_DIR
    - XML_FAILED lié au Private Parameter OUT_XML_FAILED_DIR
    - XML_LOCAL lié au Private Parameter OUT_XML_LOCAL_DIR
    - PROCESS_REPORT_MANUAL_TASKS lié au Private Parameter OUT_XLS_NOTIFICATION_DIR
    - OUT_JSON_LOCAL lié au Private Parameter OUT_JSON_LOCAL_DIR
  - Le _Workbench FME_ doit définir un Log File (accessible sous Worspace Parameters > Logging > Log file) qui doit être lié au Private Parameter LOG_FILE
  - Vous devez extraire un sous-ensemble de métadonnées qui serviront aux tests de processus. Habituellement il s'agit de la sortie du _Cutom Transformer_ Catalogue_Reader placée dans un fichier xx_catalogue_subset.ffs.  Dans tous les cas, ce fichier doit pouvoir servir d'entrée lorsqu'on utilise le _User Parameters_ IN_FFS_TESTING_FILE.  Ce fichier devrait contenir un sous-ensemble des enregistrements de métadonnées de la province (environ 10 éléments), il devrait contenir des métadonnées valides, géospatiales et non-géospatiales. Il est aussi suggérer d'éviter d'avoir le même nombre de métadonnées géo et non géospatiales afin de pouvoir plus facilement les discriminer dans les fichiers log.  Note: Un plus grand nombre de métadonées ne fera que ralentir le temps d'exécution du test de processus.

## Mise en place des répertoires

Dans le répertoire \fgp-metadata-proxy\FME_files\UNIT_TESTS\PT_HARVESTER\met vous devez créer les répertoire suivantes:

  - ..\met\ETALON\xx pour contenir les fichiers étalons utilisés par le comparateur
  - ..\met\PT_HARVESTER\xx\JSON_LOCAL pour contenir les fichiers JSON
  - ..\met\PT_HARVESTER\xx\LOG pour contenir les fichiers LOG
  - ..\met\PT_HARVESTER\xx\XLS pour contenir les fichiers EXCEL
  - ..\met\PT_HARVESTER\xx\XML_FAILED pour contenir les fichiers XML en erreur
  - ..\met\PT_HARVESTER\xx\XML_LOCAL pour contenir les fichiers XML
  - ..\met\PT_HARVESTER\xx\XML_PASSED (à créer mais pas utilisé)
  - ..\met\PT_HARVESTER\LOOKUP_TABLES\xx pour contenir les fichiers CSV et YAML de la PT

Dans le répertoire \fgp-metadata-proxy\FME_files\UNIT_TESTS\PT_HARVESTER\met vous devez copier les informations suivantes:

  - Dans ..\met\SOURCE\xx\ copier le fichier _xx_catalogue_subset.ffs_ contenant le sous-ensemble des métadonnées à traiter (créer à l'étape des Pré-conditons)
  - Dans ..\met\PT_HARVESTER\LOOKUP_TABLES\xx\ copier les fichiers CSV et YAML nécessaires pour l'exécution du processus
  - Dans ..\met\PT_HARVESTER\LOOKUP_TABLES\SHARED\ copier les fichiers CSV et YAML paratagés nécessaires pour l'exécution du processus

Mise à jour du fichier unittest.bat

  - Dans le fichier unittest.bat mettre à jour la partie interactive qui demande le nom de la PT à traiter tel que montré ci-dessous

```DOS
:begin
echo - 
echo Select a PT for the metric processus:
echo ================================
echo -
echo 1) British Columbia (BC).
echo 2) Newfound Land And Labrodor (NL)

echo -
set /p op=Select a PT (number):
SET pt_abbr=""
if "%op%"=="1" SET pt_abbr=BC
if "%op%"=="2" SET pt_abbr=NL
if "%pt_abbr%"=="" echo Invalid choice (select a number)
if "%pt_abbr%"=="" goto begin
echo on
PUSHD %Repertoire%\..
```

Pour ajouter la province de QC vous n'auriez qu'à ajouter 2 lignes tel que décrit ci-dessous: 
```DOS
:begin
echo - 
echo Select a PT for the metric processus:
echo ================================
echo -
echo 1) British Columbia (BC).
echo 2) Newfound Land And Labrodor (NL)
echo 3) Québec (QC)

echo -
set /p op=Select a PT (number):
SET pt_abbr=""
if "%op%"=="1" SET pt_abbr=BC
if "%op%"=="2" SET pt_abbr=NL
if "%op%"=="3" SET pt_abbr=QC
if "%pt_abbr%"=="" echo Invalid choice (select a number)
if "%pt_abbr%"=="" goto begin
echo on
```

## Exécution du test de processus

Pour exécuter le test de processus double cliquer sur le fichier \met\unittest.bat
La première fois que le test de processus est exécuté, il ne fonctionne pas car les répertoires étalons sont vides. Il faut copier le contenu des répertoires:
  - met\PT_HARVESTER\xx\JSON_LOCAL\*.json vers le répertoire met\ETALON\xx\JSON_LOCAL\*.json
  - met\PT_HARVESTER\xx\XML_LOCAL\*.xml vers le répertoire met\ETALON\xx\XML_LOCAL\*.xml
La deuxième fois que le test est exécuté, il devrait povoir s'exécuter sans erreur.
Le test de processus exécute deux vérifications ou tests.
  - Le premier test avec les paramètres ci-dessous crés les fichiers XML et JSON
```DOS
  - %fme% met\%Nom_Pt_App%.fmw ^
--ACTIVATE_GEO Yes ^
--ACTIVATE_NON_GEO Yes ^
--ACTIVATE_TRANSLATION No ^
--CATALOGUE_READER_SELECT No ^
--FORCED_PYCSW_URL "" ^
--IN_FFS_TESTING_FILE %in_ffs_testing_file% ^
--LOCAL_SOURCE_METADATA_DELTA_FINDER Yes ^
--LOCAL_WRITER Yes ^
--PT_ABBR %pt_abbr% ^
--METADATA_OVERWRITE Yes ^
--IN_OUT_WORKING_DIR %in_out_working_dir% ^
--SAMPLE_SIZE 0 ^
--URL_VALIDATION No
```
  - Le deuxième avec le paramètre METADATA_OVERWRITE Yes ne devrait pas recréer les fichiers XML et JSON ca ils sont déjà crééer et ils sont identiques
```DOS
  - %fme% met\%Nom_Pt_App%.fmw ^
--ACTIVATE_GEO Yes ^
--ACTIVATE_NON_GEO Yes ^
--ACTIVATE_TRANSLATION No ^
--CATALOGUE_READER_SELECT No ^
--FORCED_PYCSW_URL "" ^
--IN_FFS_TESTING_FILE %in_ffs_testing_file% ^
--LOCAL_SOURCE_METADATA_DELTA_FINDER Yes ^
--LOCAL_WRITER Yes ^
--PT_ABBR %pt_abbr% ^
--METADATA_OVERWRITE No ^
--IN_OUT_WORKING_DIR %in_out_working_dir% ^
--SAMPLE_SIZE 0 ^
--URL_VALIDATION No
```
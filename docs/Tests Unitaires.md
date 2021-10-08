# Tests unitaires dans FME

- [Mise en contexte](#Mise-en-contexte)
- [Le fichier de commandes](#Le-fichier-de-commandes)
  - [Exécution automatique des tests unitaires](#Exécution-automatique-des-tests-unitaires)
- [Contenu du fichier de commandes](#Contenu-du-fichier-de-commandes)
  - [Changement du répertoire](#Changement-du-répertoire) 
  - [Définition des noms de fichiers relatifs](#Définition-des-noms-de-fichiers-relatifs)
  - [Copie de fichiers](#Copie-de-fichiers)
  - [Concaténation des codes de retour](#Concaténation-des-codes-de-retour)
    - [Initialisation de la variable contenant les codes de retour](#Initialisation-de-la-variable-contenant-les-codes-de-retour) 
    - [Exécution de FME et capture du code de retour](#Exécution-de-FME-et-capture-du-code-de-retour)
  - [Comparaison du résultat de l'exécution avec l'étalon](#Comparaison-du-résultat-de-l'exécution-avec-l'étalon) 
    - [Comparaison avec FME](#Comparaison-avec-FME)
    - [Comparaison de fichiers ASCII](#Comparaison-de-fichiers-ASCII)
  - [Vérification de la réussite du test unitaire](#Vérification-de-la-réussite-du-test-unitaire) 

## Mise en contexte

Les tests unitaires ont pour but d'assurer du bon comportement d’un logiciel lors :

d’une modification du code;
d’une modification de la version d’un logiciel;
d’une modification de la structure des données.

Pour le logiciel FME de Safe Software les tests unitaires ont pour but de tester les Custom Transformer.  Les spécification suivantes doivent être rencontrés lorsque des tests unitaires sont développées.  Ces spécifications permettent d'augmenter le niveau de confiance dans les tests unitaires et de faciliter l'utilisation de ces tests unitaires.

- Les tests unitaires devraient minimiser les dépendances et ne devrait jamais contenir de dépendances vers des répertoires situés à l'extérieur du répertoires de tests de métriques.  Cette restriction permet d'isoler le test unitaire et d'éviter que des éléments externes viennent corrompre le test unitaire;
- Les messages d'erreurs dans le log doivent être distinct les uns des autres afin de pouvoir les extraire et les valider automatiquement à partir du fichier de commandes en lot;
- Les tests unitaires devraient être minimaliste afin de pouvoir être exécutés rapidement et être inspecté facilement; 
- Les tests unitaires devraient s'assurer de passer par les différentes intersections (*Tester*) de votre programme afin de pouvoir valider les différents scénarios possibles.  Au besoin utiliser plusieurs exécutions de FME pour tester le *custom transformer*;
- Les tests unitaires doivent utiliser des *lookup table* local et non pas ceux de production car ces derniers ne sont pas *supposer* contenir d'erreurs et sont mis-à-jour régulièrement de manière à réfléter la réalité de la production;
- Pour les sources à utiliser vous devez vous assurer que le fichier le/les fichiers sources contiennent uniquement les *features* et attributs nécessaires pour tester le *custom transformer*.  Si vous avez beaucoup de *features* sont-il vraiment nécessaires ou sont-ils redondants? Il en va de même pour les attributs, il faut conserver uniquement les attributs qui sont accédés et/ou manipulés par le *custom transformer*, les attributs supplémentaires peuvent vite devenir une source d'erreurs. Pour créer vos sources, les deux stratégies suivantes sont intéressantes: 
    - Créer un/des fichier de sources (*.ffs) minimalistes spécifiques au besoin des tests unitaires du *custom transformer*;
    - Dans le programme qui appelle le *custom transformer* utiliser le *transformer: Creator, AttributeCreator*, *Cloner*... pour créer un entrée minimaliste de *feature* et d'attributs  qui permettra de tester votre *custom transformer*.

## Le fichier de commandes

Les tests unitaires s'effectuent à partir d'un fichier de commandes en lot sur Windows (metriques.bat). Ce fichier doit contenir les commandes nécessaires à l'exécution du programme à tester ainsi que les commandes nécessaires à la vérification du résultat.

Les test unitaires se retrouvent dans le répertoire [...FME_files/UNIT_TESTS/...](../FME_files/UNIT_TESTS)

### Exécution automatique des tests unitaires

Un fichier de commandes en lot (*.bat) a été créé pour exécuter les tests unitaires sans intervention humaine Pour tous les *Custom Transformer*. Pour que ce fichier de commandes puisse utiliser un test unitaire, le .bat à exécuter doit rencontrer les exigences suivantes :

  - l'exécution du test unitaire ne requiert pas de préparation manuelle;
  - les commandes doivent être indépendantes du répertoire de développement i.e. que le nom des fichiers doit être spécifié de façon relative;
  - la procédure doit valider elle-même le résultat de l'exécution des différentes composantes du test;
  - la procédure doit retourner un code de retour 999999 (ERRORLEVEL) lorsque le test a réussi.

## Contenu du fichier de commandes

Voici les différentes sections que doit contenir le fichier de commandes pour remplir les exigences de l'exécution automatique des tests unitaires.

### Changement du répertoire 

Changement du répertoire d'exécution pour utilisation des noms de fichiers relatifs et activation des différentes variables locales

```DOS
REM ===========================================================================
REM Activer les variables locales 
REM ===========================================================================
SETLOCAL ENABLEDELAYEDEXPANSION

 
REM ===========================================================================
REM Permettre les caractères accentués
REM ===========================================================================
chcp 1252

REM ===========================================================================
REM On détermine le répertoire où se trouve le .bat et se positionne dans le 
REM répertoire plus haut tout en conservant le répertoire de départ
REM ===========================================================================
SET Repertoire=%~dp0
PUSHD %Repertoire%\..
```
### Définition des noms de fichiers relatifs

```DOS
REM ===========================================================================
REM On crée des variables contenant le nom des fichiers en mode relatif.
REM ===========================================================================
SET NomApp=RETRHN_Nettoyer_Oceans_EAnthropiques
SET fme=%FME2017%
SET FichierFmw=fme\%NomApp%.fmw
SET Comparateur=met\met_Comparateur_%NomApp%.fmw
SET FichierSOURCE=met\met_%NomApp%_SOURCE.mdb
SET FichierRESULTAT=met\met_%NomApp%_RESULTAT.mdb
SET FichierETALON=met\%NomApp%_ETALON.mdb
SET FichierLOG1=met\met_%NomApp%_EXECUTION.log
SET FichierLOG2=met\met_%NomApp%_COMPARAISON.log
```

### Copie de fichiers

Il est parfois nécessaire de copier certains fichiers avant le début des tests unitaires . Par exemple, le fichier source contient le contexte initial et le programme est conçu dans le but de modifier celui-ci. Pour conserver le fichier source intact, il faudra copier celui-ci sous un autre nom avant l'exécution du programme.

```DOS
REM ===========================================================================
REM Copie de fichiers
REM ===========================================================================
copy %FichierSOURCE% %FichierRESULTAT%
```


### Concaténation des codes de retour

Pour permettre à la procédure de valider elle-même le résultat du test, on accumule le code de retour de l'exécution de chaque étape du test dans une variable. L'exécution d'un programme retourne 0 quand tout s'est bien déroulé. Une autre valeur est retournée lorsqu'un problème survient. De cette façon, la variable contiendra une série de zéros lorsque le test est valide.

#### Initialisation de la variable contenant les codes de retour

```DOS
REM ===========================================================================
REM Initialisation de la variable qui contient le résultat de l'exécution
REM ===========================================================================
SET Statut=0
```

#### Exécution de FME et capture du code de retour

La capture du code de retour se fait en ajoutant le contenu de la variable système ERRORLEVEL au contenu de la variable Statut initialisée précédemment.

```DOS
REM ===========================================================================
REM Exécuter l'application. On détruit un fichier .LOG qui pourrait exister
REM avant l'exécution.
REM ===========================================================================
IF EXIST %FichierLOG1% DEL %FichierLOG1%
%fme% %FichierFmw% ^
 --IN_MDB_FILE %FichierSOURCE% ^
 --OUT_MDB_FILE %FichierRESULTAT% ^
 --LOG_FILE %FichierLOG1%
SET Statut=%Statut%%ERRORLEVEL%
```

Exécution de FME et capture du code de retour dans le cas où l'échec de l'exécution est le résultat attendu

Dans les cas où on teste le *transformer Terminator*, l'échec est le résultat souhaité. On doit alors chercher la présence d'une chaîne de caractères spécifiques dans le log d'exécution à l'aide de la commande FIND. Pour valider la réussite de l'exécution.

```
REM ===========================================================================
REM Exécuter l'application. On détruit un fichier .LOG qui pourrait exister
REM avant l'exécution. L'échec est le résultat attendu.
REM ===========================================================================
IF EXIST %FichierLOG1% DEL %FichierLOG1%
%fme% %FichierFmw% ^
 --IN_MDB_FILE %FichierSOURCE% ^
 --OUT_MDB_FILE %FichierRESULTAT% ^
 --LOG_FILE %FichierLOG1%

REM ===========================================================================
REM Verifier l'échec du programme avant de valider la présence du message d'erreur
REM ===========================================================================
 
IF %ERRORLEVEL% NEQ 0 (
FIND "Translation FAILED." %FichierLOG1%
SET STATUT=%STATUT%!ERRORLEVEL!
)ELSE (
SET STATUT=%STATUT%2)
```

NOTE : Si le *Terminator* retourne une chaîne particulière, vous pouvez chercher cette chaîne au lieu de *Translation FAILED*.

De plus, il est de bonne pratique d'utiliser la commande FINDSTR avec l'option /R (expression régulière). Ceci permet d'isoler les caractères accentués et autres qui sont mal interprétés lors de la comparaison.

Exemple :

```DOS
REM = Recherche à partir d'une expression régulière pour isoler <é, '>
FINDSTR /R "ERREUR.:.La.zone.utm.et.le.m.*ridien.central.n.*est.pas.identique." %FichierLOG1%
SET Statut=%Statut%%ERRORLEVEL%
```

### Comparaison du résultat de l'exécution avec l'étalon

Une fois l'exécution de l'application terminée, on doit comparer le résultat avec une copie des données attendues.

#### Comparaison avec FME

Si la comparaison se fait à l'aide du ChangeDetector, vous exécutez simplement FME en utilisant le .fmw prévu à cet effet. Pour pouvoir utiliser le code de retour, le .fmw qui fait la comparaison doit utiliser le Terminator pour faire échouer le test lorsqu'il y a des différences. De cette façon, le code de retour sera différent de zéro ce qui indiquera un échec.

ChangeDetector

```
REM ===========================================================================
REM Comparaison du RÉSULTAT avec l'ÉTALON (ChangeDetector de FME)
REM ===========================================================================
IF EXIST %FichierLOG2% DEL %FichierLOG2%
%fme% %Comparateur% ^
 --IN_RESULTAT_FILE %FichierRESULTAT% ^
 --IN_ETALON_FILE %FichierETALON% ^
 --LOG_FILE %FichierLOG2%
 SET Statut=%Statut%%ERRORLEVEL%
```


#### Comparaison de fichiers ASCII

Dans certains cas, le résultat de l'exécution de FME peut être un fichier ASCII. Dans ce cas, il est peut-être plus simple d'utiliser les commandes DOS COMP ou FC pour comparer le fichier résultant avec l'étalon. La commande COMP permet de comparer une ou plusieurs paires de fichiers. FC permet de comparer deux fichiers en ne tenant pas compte des différences de fins de lignes (CR, CRLF).


##### COMP

```
REM ===========================================================================
REM Vérification des valeurs obtenues par rapport à ce qui est attendu
REM ===========================================================================

Comparer les fichiers
ECHO N | COMP %rapport% %rapport_attendu% /A
SET Statut=%Statut%%ERRORLEVEL%
```

##### FC

```
REM ===========================================================================
REM Vérification des valeurs obtenues par rapport à ce qui est attendu
REM ===========================================================================
FC /A /L /N %rapport% %rapport_attendu%
SET Statut=%Statut%%ERRORLEVEL%
```

### Vérification de la réussite du test unitaire

Pour valider le résultat du test, il suffit de vérifier le contenu de la variable Statut. Par exemple, si le test est composé de deux exécutions de FME plus l'exécution d'un comparateur, l'accumulation des codes de retour en cas de réussite donnera 000. En y ajoutant la valeur 0 de l'initialisation, la variable Statut contiendra donc 0000 lorsque le test est réussi. On peut alors gérer la sortie de la procédure.

```DOS
@IF [%Statut%] EQU [0000] (
 @ECHO INFORMATION : Test de métrique réussi
 @COLOR A0
 @SET CodeSortie=999999
) ELSE (
 @ECHO ERREUR : ERREUR, test de métrique échoué
 @COLOR CF
 @SET CodeSortie=-1
)

REM ===========================================================================
REM On ramène la fenêtre dans le répertoire de départ
REM ===========================================================================
POPD
 
REM ===========================================================================
REM On fait une pause pour ne pas que la fenêtre se ferme au cas où
REM on aurait double-cliquer sur le .bat pour l'exécuter
REM ===========================================================================
PAUSE
COLOR
EXIT /B %CodeSortie%
```

Destruction des tables SDE des comptes Métrique

Si pour un test de métrique, vous avez crée des tables spatiales, il est recommandé de faire le ménage à la fin de votre test. Pour détruire une table spatiale,il ne suffit pas de faire un "Drop Table" car cette opération corrompt la cartouche SDE. Il est plutôt prescrit d'utiliser le programme python DetruireTableSDE.py qui détruit correctement les tables spatiales.


Exemple d'utilisation dans un test de métrique:

```DOS
REM ================================
REM Destruction (drop) des tables spatiales
REM ================================
 
ECHO Création du fichier de connexion .sde
SET SERVEUR=sdehost.cits.rncan.gc.ca 
SET SERVICE=sde:oracle11g:prod_dev
SET USERNAME=metriques
SET PASSWORD=dev
 
SET REP_SDE=%FME_TEMP%
SET NOM_SDE=connexion_%NomApp%.sde
 
%python27% -c "import arcpy; arcpy.CreateArcSDEConnectionFile_management(r'%REP_SDE%', '%NOM_SDE%', '%SERVEUR%', '%SERVICE%', '', 'DATABASE_AUTH', '%USERNAME%', '%PASSWORD%')"
SET Statut=%Statut%%ERRORLEVEL%
 
SET TABLES_SPATIALES_A_DETRUIRE=SYS_ZT_2,SYS_ZTE_2,POLYGONE_CREERZTE_2,POINT_CREERZTE_0,LIGNE_CREERZTE_1
 
ECHO Destruction des tables spatiales...
%python27% \\dfscitsh\cits\EnvCits\applications\cits\pro\py\DetruireTableSde.py "%REP_SDE%\%NOM_SDE%" "%TABLES_SPATIALES_A_DETRUIRE%"
SET Statut=%Statut%%ERRORLEVEL%
 
DEL %REP_SDE%\%NOM_SDE%
```


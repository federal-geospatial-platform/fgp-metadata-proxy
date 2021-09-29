Les tests unitaires ont pour but d'assurer du bon comportement d’un logiciel lors :

d’une modification du code;
d’une modification de la version d’un logiciel;
d’une modification de la structure des données.

Pour le logiciel FME de Safe Software les tests unitaires ont pour but de tester les Custom Transformer.  Les spécification suivantes doivent être rencontrés lorsque des tests unitaires sont développées.  Ces spécifications permettent d'augmenter le niveau de confiance dans les tests unitaires et de faciliter l'utilisation de ces tests unitaires.

  - Le tests unitaires devrait minimiser les dépendances et ne devrait jamais contenir de dépendances vers des répertoires situés à l'extérieur du répertoires de tests de métriques.  Cette restriction permet d'isoler le test unitaire et d'éviter que des éléments externes viennent corrompre le test unitaire;
  - Les messages d'erreurs dans le log doivent être distinct les uns des autres afin de pouvoir les extraire et les valider automatiques à partir du fichier de commandes en lot;
  - Les tests unitaires devraient être minimaliste afin de pouvoir être exécutés rapidement et être inspecté facilement; 
  - Les tests unitaires devraient s'assurer de passer par les différentes intersections de votre programme afin de pouvoir valider les différents scénarios possibles.  Au besoin utiliser plusieurs exécutions de FME pour tester le *custom transformer*;
  - Les tests unitaires doivent utiliser des *lookup table* local et non pas ceux de production car ces derniers ne sont pas *supposer* contenir d'erreurs et sont mis-à-jour régulièrement de manière à réfléter la réalité de la production.

metriques.bat

Les tests unitaires s'effectuent à partir d'un fichier de commandes en lot sur Windows (.bat). Ce fichier doit contenir les commandes nécessaires à l'exécution du programme à tester ainsi que les commandes nécessaires à la vérification du résultat.

Les test unitaires se retrouvent dans le répertoire [...FME_files/UNIT_TEST/...](../UNIT_TESTS)

Exécution automatique du test

Un fichier de commandes en lot (*.bat) a été créé pour exécuter les tests unitaires sans intervention humaine Pour tous les *Custom Transformer*. Pour que ce fichier de commandes puisse utiliser un test unitaire, le .bat à exécuter doit rencontrer les exigences suivantes :

  - l'exécution du test unitaire ne requiert pas de préparation manuelle;
  - les commandes doivent être indépendantes du répertoire de développement i.e. que le nom des fichiers doit être spécifié de façon relative;
  - la procédure doit valider elle-même le résultat de l'exécution des différentes composantes du test;
  - la procédure doit retourner un code de retour 999999 (ERRORLEVEL) lorsque le test a réussi.

Contenu du .bat

Voici les différentes sections que doit contenir le fichier de commandes pour remplir les exigences de l'exécution automatique des tests unitaires.

```dos
Changement du répertoire d'exécution pour utilisation des noms de fichiers relatifs et activation des variables locales
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

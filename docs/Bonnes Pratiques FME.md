# Bonne Pratiques FME

Ce document contient une liste de bonne pratiques à utiliser lors du développement de *Workbench* ou de *Custom Transformer*.  Le suivi de ces directives facilitera la maintenance en assurant un homogénéité du code écrit par les différents développeurs.

Note importante: Ce document de bonne pratiques FME est en mode ébauche, les membres de l'équipe sont encouragés à développer de nouvelles *bonnes pratiques FME* ou de bonifier des *bonne pratiques FME* existentes qui seront partagées au sein de l'équipe et consignées dans le site web d'équipe.   

Ce document adresse les éléments de *bonnes pratiques FME* suivants:

 - [Création de custom transformer](#Création-de-custom-transformer)
 - [Documentation](#Documentation)
 - [Enregistrement entrant et sortant](#Enregistrement-entrant-et-sortant)
 - [Gestion des attributs](#Gestion-des-attributs)
 - [Hardcoding](#Bookmark)
 - [Nom du transformer](#Nom-du-transformer)
 - [Résillience](#Résillience)
 - [Terminator](#Bookmark-imbriqué)
 - [Tester ou TestFilter](#Tester-ou-TestFilter)


# Création de custom transformer

Le *custom transformers* est une composante essentielle pour écrire du code réutilisable et développer des *workbench* qui sont plus facilement lisibles et maintenables.  Le *custom transformer* permet d'encapsuler (d'isoler) du code qui est un concept important de la programmation moderne.

La compagnie FME offre plusieurs [tutorials](https://docs.safe.com/fme/html/FME_Desktop_Documentation/FME_Workbench/Workbench/custom_transformer_creating.htm) et [vidéos](https://www.youtube.com/watch?v=oQ_SeW0sdEM&ab_channel=MarkIreland) montrant comment développer des *custom transformer*.  A ces bonnes pratiques, il faut ajouter les particularités suivantes qui touchent l'utilisation des *custom transformer* dans notre organisation.

  - Lorsque l'on crée un *custom transformer* avec la commande *Export as Custom Transformer* vous devez toujours vous assurez que l'option *Insert mode* est **Linked by default** ce qui permet de garder un lien vers le *custom transformer* et non pas de l'incorporer dans votre code.  De cette façon si le *custom transformer* est modifié vous aurez toujours un lien vers la version la plus récente.

![Export curtom](images/img_6.png)

  - Lorsque le *custom transformer* est exporté vous devez ajusté le mode d'exécution dans Python.  Pour ce faire, dans le panneau *Navigator*, *Transformer Parameters* > *Scripting* > *Python compatibility* mettre la valeur **Python 3.7+**

![Set python](images/img_7.png)

# Documentation

Toujours documenter les *transformer* et *custom transformer* selon la [procédure de documentation](Documentation%20FME.md) afin d'assurer une homogénéité dans le code en plus de maximiser sa lisibilité.
 

# Enregistrement entrant et sortant

Dans un *custom transformer* le nombre d'enregistrement entrant devrait habituellement être égal au nombre d'enregistrement sortant.  Si vous avez des enregistrements problématique, il est préférable d'avoir un ou plusieurs ports de sortie dédiés pour gérer ces cas (ex.: *Error* ou *Unprocessable*) afin de laisser au *workbench* ou *custom transformer* appelant la décision de comment gérer ces cas problématiques: en les enregistrant dans un fichier de log ou en appelant un *Terminator* ou autre moyen de gestion des cas problématiques.


# Gestion des attributs

Le traitment des collections d'enregistrements de métadonnées des différentes provinces utilise plusieurs centaines d'attributs FME et de listes FME en plus de ceux qui sont créés par les différents *transformer* et *custom transformer* de vos *workbench*.  En plus de saturer le FME Data Inspector et de rendre l'interprétation des résultats plus difficile, les attributs et listes sont de grands consommateurs de ressources pour FME (mémoire et CPU).  Afin de mieux gérer les attributs tous les *custom transformer* doivent se conformer aux directives suivantes:
  * Utiliser le *custom transformer* ATTRIBUTE_UNEXPOSER à la fin de l'exécution d'un *custom transformer* afin qu'aucun n'attribut ne soit exposé;
  * Utilisé le *transformer* *AttributeExposer* au début de votre *custom transformer* afin d'exposer uniquement les attributs nécessaires à votre traitement afin d'en faciliter la lecture, le débuggage et optimiser l'utilisation des ressources;
  * Utiliser le *AttributeRemover* afin d'enlever tous les attributs et listes temporaires et/ou qui ne sont plus utiles à votre traitement subséquents afin d'en faciliter la lecture, le débuggage et optimiser l'utilisation des ressources.


# Hardcoding

Le *hardcoding* est une pratique de développement logiciel où les données sont directement écrite dans le code.  Cette pratique tend à créer du code moins générique qu'il faut constamment modifier pour l'adapter à de nouvelles situations (ex.: prise en charge de nouvelles provinces).  Le *hardcoding* est à éviter à tout prix.  L'utilisation de fichiers de configuration et de *publish parameters* est encouragée afin d'éviter les problèmes engendrés par le *hardcoding*.

C'est au développeur d'identifier les situations potentielles de *hardcoding* et de choisir la meilleure stratégie d'évitement.


# Nom du transformer

Toujours conserver le nom du *transformer* tel que donné par FME.  Si vous avez plus d'un *transformer* du même type dans votre *workbench* alors ajouter un suffixe numérique (ex pour le *transformer* Tester: Tester, Tester_1, Tester_2, ...).  Conserver le nom du *transformer* original permet d'identifier plus rapidement le type de *transformer* employé.  Si un nom plus représentatif vous semble important alors privilégier une annotation sur le *transformer*. 


# Résillience

Le traitement des collections d'enregistrements de métadonnées de l'environnement des provinces et territoires (P/T) à celui du gouvernment fédéral se fait par traitment en lot (via *FME Server*).  Il est donc primordial que tous les *workbench* qui traitent les différentes P/T soient très résillients aux problèmes.  Si un ou plusieurs enregistrments de métadonnées ne peuvent pas être traduits car ces derniers contiennent un ou plusieurs cas particuliers qui ne sont pas pris en compte, il faut alors rejeter ce ou ces enregistrments, laisser une trace du problème dans un fichier log et traiter tous les autres enregistrements que le workbench est capable de manipuler.  Dans ce type de condition, il ne faut pas utiliser de *Terminator* qui ferait arrêter abruptement l'exécution du programme. 

**C'est au développeur de trouver la juste balance entre quand utiliser le *Terminator* (faire terminer abruptement un programme) car un *workbench* est dans un état instable et quand un *workbench* est incapable de traîter un enregistrement de métadonnées et ce dernier doit simplement être rejeté.**


# Terminator

Le *Terminator* est un *transformer* qui arrête abruptement l'exécution du *workbench* lorsqu'il est activé.  Il est utilisé généralement pour détecté des situations non valides.  Le *terminator* devrait toujours être utilisé dans le cas de *transformer* lorsqu'une situation inattendue survient mais aussi dans le cas de *transformer* qui possèdent plusieurs ports de sortie qui ne devraient pas être utilisé normalement. Dans de tels cas les ports de sortie *non utilisés* devraient être reliés à un *Terminator* de façon à déceler ces cas dans le code (voir figure ci-dessous).

Le *Terminator* offre aussi la possibilité d'afficher un texte lorsqu'il est activé.  Le texte devrait toujours être représentatif de la raison pourquoi le *Terminator* est activé (ex.: *Invalid attribute value for ID*) et éviter les formalutation trop générique (ex.: *Translation failed...*)

![Terminator usage](images/img_5.png)


# Tester ou TestFilter

Les *transformer* *Tester* et *TestFilter* offre des capacités similaires pour tester des attributs et aiguiller l'exécution du programme.  Par contre, le transformer *TestFilter* offre les avantages suivants: 
  - Permet de par sa structure de fusionner plusieurs *transformer* *Tester* en un seul *transformer* *TestFilter* ce qui allège l'espace de travail; 
  - Permet d'utiliser plusieurs ports de sortie comme un outil *case* ou *switch* alors que *tester* n'offre que 2 ports de sortie (*Passed/Failed*);
  - Offre la possibilité de nommer les ports de sortie ce qui permet souvent d'autodocumenter le *tranformer*
  - Offre la possibilité d'avoir un port de sortie spécial (ex.: *Unfiltered*) pour gérer les cas non traités.  Vous pouvez alors utiliser un *Terminator* pour gérer tous ces cas problématiques.

En résumé, utiliser *Tester* pour des tests binaires (True|False) qui conviennent bien à leur port de sortie (*Passed/Failed*). Privilégié *TestFilter* pour les autres cas pour diminuer le nombre de transformer et augmenter la lisibilité.

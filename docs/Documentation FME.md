# Documentation FME


Les directives de documentation contenues dans ce document ont pout but d'assurer une homogénéité dans le code produit par les différents membres de l'équipes en plus de maximiser la lisibilité, l'usage et la maintenance.

Ce document adresse les éléments de documentation suivants:

 - [Annotation](#Annotation)
 - [Bookmark](#Bookmark)
 - [Bookmark imbriqué](#Bookmark-imbriqué)
 - [Description](#Description)


# Annotation

L'annonations est l'élément de base de la documentation dans FME.  N'hésitez pas à ajouter une annotation à pratiquemment tous vos *transformers* dans votre *workbench* ou *custom transformer*.  Ce qui est trivial lorsqu'on écrit du code aujourd'hui peut devenir moins trivial pour une autre personne ou pour vous même dans quelques semaines.  

De bonnes annotations permettent aussi de suivre et comprendre plus facilement le déroulement d'un *workbench* ou d'un *custom transformer* sans avoir à toujours cliquer dans les différentes boîtes pour les ouvrir et en comprendre le comportement.  Pour des annotation plus complexes, il est possible de placer des hyper liens et de changer le style du texte.

![img_3.png](img_3.png)

# Bookmark

Le *bookmark* (signet) est un élément visuel puissant qui permet de regrouper ensemble des *transformers* qui forment une unité de traitement.  Les *bookmarks* permettent de simuler des sous-routines.  Vous devriez toujours ajouter une courte phrase qui résume ce qui s'exécute dans le *bookmark*.  Vous pouvez aussi donner une couleur à votre *bookmark*, ce qui permet de les localiser plus rapidement et d'organiser votre espace de travail.

Les *bookmark* jouent un rôle important dans FME pour plusieurs raisons :
  * Comme marqueur pour un accès rapide à certaines zones de votre *workbench* ou *custom transformer*;
  * Pour diviser un espace de travail en différentes sections clairement marquées;
  * Pour organise un *workbench* ou *custom transformer* afin que vous puissiez déplacer plusieurs *transformers* en même temps;
  * Pour facilite la gestion des grands espace de travail en réduisant (*collapse*) les *transformer* qui sont placés dans en *bookmark*.

La figure ci-sessous montre un exemple d'utilisation de *bookmark* pour diviser l'espace de travail et mettre en relief les différentes tâches effectuées:

![img.png](img.png)

# Bookmark imbriqué

Il est possible d'imbriquer des *bookmark* les uns dans les autres.  ce qui permet d'ajouter une dimension supplémentaire dans le regroupement de tâches similaires dans un espace de travail volumineux.

# Description

Tous les *workbench* et *custom transformer* doivent être documentés.  L'application FME offre des outils intégrés qui facilite la documentation.  On retrouve ces outils dans la fenêtre Navigator sous l'onglet Transformer Parameters > Description (voir image cidessous)

![img_1.png](img_1.png)

Cliquer sur Overview et la fenêtre ci-dessous va apparaître:

![img_2.png](img_2.png)

Vous devez remplir le champ  *Category* avec la valeur *FGP Tools* (habituellement), l'onglet Overview et l'onglet History.

L'onglet *Overview* doit contenir les informations suivantes

<u>**Description**</u>

  * Inclure une decription détaillée du *custom transformer*.  La description doit mettre l'emphase sur ce que fait (*le quoi*) le *workbench* ou le *custom transformer* plutôt que sur le comment les choses sont faites.

  * Au besoin décrire les pré-conditions nécessaires à l'exécution du *custom transformer*

 
<u>**Input Ports**</u>

  * Décrire de façon détaillée le contenu de tous les ports d'entrées (*input ports*) du *custom transformer*. Si votre *custom transformer* ne contient qu'un seul port d'entrée, il devrait simplement être nommé *Input*


<u>**Output Ports**</u>

  * Décrire de façon détaillé le contenu de tous les ports de sorties (*output ports*) du *custom transformer*. Si votre *custom transformer* ne contient qu'un seul port de sortie, il devrait simplement être nommé *Output*


<u>**Parameters**</u>

  * Description détaillée de chaque paramètres du *custom transformer*.  Inscrire la valeur par défaut, si le paramètre contient une liste de valeurs (ex.: YES|NO), il faut documenter le comportement attendu de chaque valeur. 


<u>**Note**</u> ou <u>**Usage**</u> *(Sections optionnelles)*

  * Les sections *Note* et/ou *Usage* sont facultatives et devraient être seulement utilisés lorsque de l'information aditionnelle est requise pour aider à la comprhension du *custom transformer*.


L'onglet *History* contient l'historique des travaux fait sur un *workbench*ou un *custom transformer*.  Normalement à chaque fois que le *custom transformer* est publié ou republié dans le dépôt GitHub, on devrait ajouter une ligne dans l'historique.  Cet onglet contient la date du développement, le nom du développeur et un commentaire (pour la première version, on peut écrire "Version originale")

Note: Les *custom transformer* JSON_PUBLISHER et XML_PUBLISHER sont de bons exemples pour la documentation.

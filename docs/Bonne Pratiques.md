# Bonne Pratiques FME

Ce document contient une liste de bonne pratiques à utiliser lors de la conception de *Transformer* ou de *Custom Transformer*.  Le suivi de ces directives facilitera la maintenance du code en assurant un homogénéité du code écrit par les différents développeurs.

Ce document de bonne pratiques est en mode ébauche, les membres de l'équipe sont encouragés à développer de nouvelles *bonnes pratiques* ou bonifier des *bonne pratiques* qui seront partagées au sein de l'équipe et consignées dans le site web d'équipe.   

Ce document adresse les éléments de *bonnes pratiques* suivants:

 - [Documentation](#Documentation)
 - [Hard coding](#Bookmark)
 - [Terminator](#Bookmark-imbriqué)
 - [Unexposer](#Description)


# Documentation

Afin d'assurer une homogénéité dans le code produit par les différents membres de l'équipes en plus de maximiser la lisibilité et l'usage tous les *transformer* et custom transformer*
Toujours documenter les CT avec la [procédure de documentation des CT](Documentation%20FME.md) 

 

Jamais de hardcoding dans le code toujours utiliser des fichiers de config 

 

Toujours écrire les items non traitables dans un fichier log.  Le FME ne doit jamais planter à moins d'une erreur  

 

Si on utilise un transformer Terminator ne pas seulement écrire Translation Terminated mais décrire la raison de l'erreur 

 

À la fin desw traitment toujours utiliser le attribute unexposer 
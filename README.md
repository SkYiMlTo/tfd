<code> [This page is written in french, if you don' t understand this language, feel free to contact me and I'll explain you ;)]</code>
# TechnoFlexDétente Project
Leurs réseaux sociaux:  
<a href="https://open.spotify.com/user/3125yxg52epfvjn26ih6h6mzjvdu?si=0d4b571dc7fa4dc4"><img src="https://user-images.githubusercontent.com/51914435/146079798-ed8d886f-81df-4581-aa3b-626e49124c34.png" alt="Spotify logo" width="25" height="25"></a><code>Spotify</code>  
<a href="https://discord.gg/xSp4z5aStx"><img src="https://user-images.githubusercontent.com/51914435/146083739-91a491de-8a4e-49a9-bb3b-bbe4cee5ce61.png" alt="Discord logo" width="25" height="25"></a><code>Discord</code>  
<a href="https://www.facebook.com/technoflexdetente"><img src="https://user-images.githubusercontent.com/51914435/146082875-9915bcf7-e6dd-414e-9f7c-0f68e6802948.png" alt="Facebook logo" width="25" height="25"></a><code>Facebook</code>  
<a href="https://www.instagram.com/technoflexdetente/"><img src="https://user-images.githubusercontent.com/51914435/146082880-ab991b74-e77e-4738-bdbc-aa76af8109c0.png" alt="Instagram logo" width="25" height="25"></a><code>Instagram</code>  
  
## Qui est TechnoFlexDétente?
Il s'agit d'un groupe dans l'événementielle.  
Sur les différents médias où ils sont présents, vous pourez trouver différentes informations telles que:
- Des informations sur les soirées à venir (en fonction des régions)
- Une communauté soudée
- Partage de musiques (tracks)
- Moyens de transport
- Vente / Achat de matériel
- Vente / Achat de place pour différents événements

## Pourquoi ce projet ?
Pour un groupe basé dans l'événementiel avoir un moyen de partage de musique au sein de la communauté est fortement souhaité. Lorsque l'on créé des playlists collaboratives sur Spotify tout le monde peut ajouter des musiques, ce aui répond bien à la demande. Cependant, tout le monde peut aussi en supprimer, c'est là qu'intervient ce projet...

## Quel est le but
L'objectif est de pouvoir gérer différentes playlists (en fonction des styles de musique) sur Spotify et que tout le monde puisse ajouter des musiques dans les catégories qu'il désire. Le code va faire en sorte de synchroniser les musiques ajoutées toutes les minutes.

## Fonctionnalités
- Si une personne supprime des musiques, elle reviendront automatiquement.
- Le script aura aussi pour rôle de supprimer les doublons.
- Les administrateurs pourront supprimer des musiques directement depuis le compte.

## Fonctionnement
Sur le profil du compte spotify de TechnoFlexDetente nous pouvons observer différentes playlists collaboratives.
![image](https://user-images.githubusercontent.com/51914435/146085967-a9003369-47c6-4b83-af83-be425ad80b1f.png)
Le code va fonctionner avec différentes playlists cachées pour synchroniser les sons. Dans le code on peut retrouver différentes notations C et NC signifiant respectivement collaborative et non collaborative. C'est un moyen pour se retrouver entre les différentes playlists. Chaque playlist aura donc un doublon caché permettant d'effectuer les synchronisations. C'est dans les playlists non collaboratives que les administrateurs auront la possibilité de supprimer des musiques.  
Plutôt que d'utiliser des playlists cachées nous aurions pu effectuer des synchronisations sur la partie serveur, il aurait fallu trouver une autre implémentation pour que les administrateurs puissent supprimer des sons.  
  
Pour ce qui est de la communication entre le script et le serveur, c'est l'API de spotify qui est utilisée

## Améliorations à venir
Synchronisations des playlists avec celle d'un compte Deezer.

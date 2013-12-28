## Installation global via pip 

### Installation sur python3
```bash
sudo pip3 install pycis.tar.gz
```

### Installation sur python2 (pas recommandé)
```bash
sudo pip install pycis.tar.gz
```

## l'installation dans une env (facultatif: Si tu prefère installer dans une env)

```bash
# créer un environment virtuel de python3
virtualenv -p /usr/bin/python3 env_pycis

# rentrer dans l'environment virtuel
cd env_pycis

# activer l'environment virtuel
source bin/activate

# decompresse le tar(joint au mail) dans le dossier du environment virtuel 
# tu peux faire avec dolphin ou avec terminal "tar zxvf pycis.tar.gz"
pip install pycis.tar.gz
```

## Utilisation:

Une fois installé, tu vas avoir un script appelé pycis-cli. Avec ce script tu pourras interagir avec l'interface de pycis

### Rentrer au mode iteractive (Seulement sur python3)

```bash
pycis-cli 
```

###### Faire recherche

```bash
(pycis) search Eat Pray Love
#[1] resultat
#[2] resultat 2
```

###### Trouver urls pour un des resultats

```bash
(pycis) get 1
# http://example.com
# http://example.com/2
# http://example.com/3
```

###### Trouver de l'aide dans le mode iteractive

```bash
(pycis) help
```

###### Trouver de l'aide dans le mode iteractive pour une commande, 

```bash
# ex: pour la commande 
(pycis) help search

# ex: pour la get 
(pycis) help get
```

### Pour faire extraction d'URLs pour un episode choisi, utilises l'argument `-de` ou `--download-episode`

```bash
# ex: Télécharger directement "Vampire Diaries" Saison 5 Episode 1
pycis-cli -s "vampire diaries" -de s05e01
```

```bash
# ex: Télécharger directement "Teen Wolf" Saison 1 Episode 10
pycis-cli -s "teen wolf" -de s01e10

# Alternative
pycis-cli -s "teen wolf" --download-episode s01e10
```

### Pour regarder la video directement sur VLC sans télécharger, argument `-p` ou `--play`. Pour voir sur une autre application à la place de VLC, utilises l'argument `--player` suivi du nom de l'application.

```bash
# ex: Régarder directement "Game of Thrones" Saison 3 Episode 9 et être super choqué avec le marriage rouge, :D
pycis-cli -s "game of thrones" -de s03e09 -p

# Alternative
pycis-cli -s "game of thrones" -de s03e09 --play

# Pour regarder sur une autre application video, ex: mplayer
pycis-cli -vv -s "game of thrones" -de s03e09 -p --player mplayer
```

### Pour avoir de l'aide sur les commandes, argument `-h` ou `--help`

```bash
pycis-cli -h

# Alternative
pycis-cli --help
```


### pour debugger un probleme après une installation reussi argument `-vv` ou `--verbose`. (ex: pycis a marché une fois mais maintenant il a des erreurs)

```bash
pycis-cli -s "vampire diaries" -de s05e03 -vv

# Alternative
pycis-cli -s "vampire diaries" -de s05e03 --verbose
```

## Résoudre des problèmes:

#### Le programme ne quites jamais, il est en train de clignoter le curseur il y a plus de 30 seconds

Fais CTRL+C

#### Tu ne sais pas quitter le mode iterative

Penses à Ruby, :D

#### Si il y a d'autres erreur tapes ça:

```bash
Notre Père
Qui es aux Cieux
Que Ton Nom soit sanctifié
Que Ton Règne vienne
Que Ta Volonté soit faite sur la terre comme au ciel
Donne-nous aujourdhui notre pain de ce jour
Pardonne nous nos offenses comme nous pardonnons aussi à ceux
qui nous ont offensés
Et ne nous laisse pas entrer en tentation
Mais délivre-nous du mal
Car c'est à Toi qu'appartiennent : le Règne, la Puissance et la Gloire
Pour les siècles des siècles

Amen!
```

## Bonus:

![je taime](http://images2.fanpop.com/image/photos/13800000/Key-to-my-Heart-speter-13806362-1280-800.jpg)
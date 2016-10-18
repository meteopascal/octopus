## octopus

Serveur permettant d'interroger une base
sqlite et d'afficher les résultats.

Stage Python intermédiaire, du 10 au 13 octobre 2016.


### git

Accès à github
- en lecture seule par https : `git clone https://github.com/meteopascal/octopus.git`
- en lecture/écriture par ssh: `git clone git@github.com:meteopascal/octopus.git`

Pour l'accès par ssh, envoyez-moi votre clef publique par mail, en vous inspirant de:
```
mail -s 'accès github à octopus' pascal.lamboley@meteo.fr < ~/.ssh/id_rsa.pub
```
 
On a utilisé pendant le stage un dépôt local (le ssh sortant est filtré à l'ENM...)

Il a fallu changer l'url de notre copie de travail, qui pointait sur github:
```
git remote set-url origin ~lamboleyp/gitrep/octopus.git
```

ce qui nous a obligé à redonner les droit d'écriture aux autres participants après un commit:
```
chmod -Rc ug+w ~lamboleyp/gitrep/*.git
```


### lancement du serveur (version j3)
```
python3 server.py
```
Puis lancer un navigateur sur [http://localhost::8080](http://localhost:8080)


### base de données (version j3)

Pour récupérer la base (230 Ko):
```
cp ~lamboleyp/dev/octopus/Sites.sqlite ./
```

Exemple d'instanciation de la classe `SitesDb`
```
from db import SitesDb
d = SitesDb("Sites.sqlite")
```

Exemple d'insertion d'un nouveau site
```
monsite = dict(
    cccc='toul',
    ii=31,
    wmo_id=31000,
    wmo_id_bufr_fr=31001,
    site_name='toulouse',
    region_num=12,
    MF_identifier='toul',
    latitude_wgs84=44.0,
    longitude_wgs84=1.0,
    altitude_site=132.0,
    tower_height=47,
    id_radar_model=458,
    nom_fichier_altitudeterrain='toto',
    DPOL_hardware_mode=54,
    indicateur_panne=0,
) 
d.add_site(monsite)
```

Exemple de sélection par la localisation (latwidth, lonwidth optionnels, par défaut fixées à 3)
```
lat = 46
lon = 2
d.get_by_loc(lat, lon, latwidth=3, lonwidth=3)
```

### jour 4
J'ai mis là les deux essais réalisés:
  * un serveur `flask`, qui lit des données en .csv via `pandas`, et les met en forme avec `jinja2`.
  * un accès générique à la base, qu'elle soit sous `MySQL`, `PostgreSQL` ou `Sqlite`, grâce à l'ORM `SQLAlchemy`.

Le fichier `requirements.txt` est sans aucun doute beaucoup trop complet, mais il contient _aussi_
le nécessaire : on y retrouvera le nom de la bibliothèque à utiliser pour l'installer.

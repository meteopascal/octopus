# octopus

Serveur permettant d'interroger une base
sqlite et d'afficher les résultats.

Pour récupérer la base (230 Ko):
    cp ~lamboleyp/dev/octopus/Sites.sqlite ./
    
## base de données
exemple d'instanciation de la classe `SitesDb`
```
from db import SitesDb
d = SitesDb("Sites.sqlite")
```
exemple d'insertion d'un nouveau site
```
monsite = {'cccc':'toul',
'ii':31,
'wmo_id':31000,
'wmo_id_bufr_fr':31001,
'site_name':'toulouse',
'region_num':12,
'MF_identifier':'toul',
'latitude_wgs84':44.0,
'longitude_wgs84':1.0,
'altitude_site':132.0,
'tower_height':47,
'id_radar_model':458,
'nom_fichier_altitudeterrain':'toto',
'DPOL_hardware_mode':54,
'indicateur_panne':0,
'id_radar_model':5} 
d.add_site(monsite)
```

exemple de selection par la localisation
latwidth, lonwidth par défaut fixées à 3

```
lat = 46
lon = 2
d.get_by_loc(lat, lon[, latwidth, lonwidth])
```

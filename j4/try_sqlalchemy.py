#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Préparation:
  * sqlite: la table 'SITES' de la base 'Sites.sqlite' contenait des clefs étrangères,
    inutilisables en l'absence de l'autre table référencée. On a enlevé ces colonnes
    avec le plugin "Sqlite Manager" de Firefox (click droit / drop)
    On a aussi renommé la table de "SITES" en "Sites", c'est plus joli.
  * postgresql: on a exporté la table Sites (dans Sqlite Manager, menu exporter en
    sql), et importé le Sites.sql résultant avec pgadmin3.
  * mysql: le sql ne convenait pas à phpMyAdmin, on lui a fait un csv. Et on a fait
    une clef primaire de 'id_site', sinon la table n'est pas accessible en automap.
"""

import os
import pprint

from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy.schema import Table, MetaData

# prevent PyCharm formatter from removing these imports, even if unused
assert any([pprint, os, Table, MetaData, ])


def is_ipython():
    """Tell if we are in iPython."""
    try:
        assert __IPYTHON__
        return True
    except NameError:
        pass
    return False


def test_alchemy(url):
    # un moteur capable de se connecter à notre base
    engine = create_engine(url)

    # la base, en mode "découverte et introspection"
    base = automap_base()
    base.prepare(engine, reflect=True)

    # les noms des tables disponibles dans la base
    available_tables = base.metadata.tables.keys()
    print('available_tables: ', available_tables)

    # on choisit une table, ici par son nom
    table_name = 'Sites'
    table = base.classes.get(table_name)

    # les colonnes disponibles dans cette table
    # variante: keys = table.__mapper__.attrs.keys()
    keys = base.metadata.tables.get(table_name).columns.keys()
    print('columns:', keys)

    # digression - aller chercher les clefs dans
    #     base.metadata.tables.get(table_name)
    # nous donne envie d'écrire, et ça marche:
    #     table = base.metadata.tables.get(table_name)
    #     keys = table.columns.keys()
    # Mais la table que l'on obtient ainsi n'est pas la même que
    # ``base.classes.get(table_name)`` que nous avons retenue plus
    # haut: elle n'est pas "mappée" et ce qui suit ne fonctionne
    # pas avec elle (ORM = Object Request Mapper).

    # interrogation sans sql, exprimée en Python grâce au mapping
    latmin, latmax = 43, 45
    lonmin, lonmax = -2, 2
    query = Session(engine).query(table)
    selected = query.filter(
        table.latitude_wgs84 >= latmin,
        table.latitude_wgs84 <= latmax,
        table.longitude_wgs84 >= lonmin,
        table.longitude_wgs84 <= lonmax
    )
    print()
    for site in selected:
        dico = {k: site.__getattribute__(k) for k in keys}
        print('site_name', site.site_name, dico)

    # la requête réellement effectuée est str(selected):
    print('\n', selected)


if __name__ == '__main__':
    # iPython ne démarre pas où il faut
    if is_ipython():
        os.chdir('octopus/j4')

    # Choix de la base à lire. Pas d'autre changement dans
    # le code pour peu que les bases soient équivalentes.
    url = "sqlite:///Sites.sqlite"
    # url = "mysql://stage:stage@localhost/test"
    # url = "postgresql://stage:stage@localhost/test"

    test_alchemy(url)

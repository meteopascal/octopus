#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3


class SitesDb(object):
    """Classe de gestion de la bdd Sites."""

    def __init__(self, path):
        self.db = sqlite3.connect(path)
        self.cursor = self.db.cursor()

    def get_all(self):
        tous = self.cursor.execute('''SELECT * FROM SITES''').fetchall()
        return self.list_to_dict(tous)

    def get_by_id(self, index):
        one = self.cursor.execute('''SELECT * FROM SITES WHERE id_site=''' + str(index)).fetchone()
        return self.row_to_dict(one)

    def add_site(self, dct):
        self.cursor.execute('''INSERT INTO SITES (nom_fichier_altitudeterrain, tower_height,
            MF_identifier, wmo_id, longitude_wgs84, ii, site_name, id_radar_model, indicateur_panne,
            cccc, latitude_wgs84, DPOL_hardware_mode, altitude_site, region_num, wmo_id_bufr_fr)
            VALUES(:nom_fichier_altitudeterrain, :tower_height, :MF_identifier, :wmo_id,
            :longitude_wgs84, :ii, :site_name, :id_radar_model, :indicateur_panne, :cccc,
            :latitude_wgs84, :DPOL_hardware_mode, :altitude_site, :region_num, :wmo_id_bufr_fr)''', dct)
        self.db.commit()

    def row_to_dict(self, row):
        d = {}
        for idx, col in enumerate(self.cursor.description):
            d[col[0]] = row[idx]
        return d

    def list_to_dict(self, listeinput):
        # return [self.row_to_dict(row) for row in listeinput]
        listeoutput = []
        for row in listeinput:
            listeoutput.append(self.row_to_dict(row))
        return listeoutput

    def get_by_loc(self, lat, lon, latwidth=3, lonwidth=3):
        latmin = lat - latwidth / 2.0
        latmax = lat + latwidth / 2.0
        lonmin = lon - lonwidth / 2.0
        lonmax = lon + lonwidth / 2.0
        tous = self.cursor.execute('''SELECT * FROM SITES
                WHERE latitude_wgs84>{}
                  AND latitude_wgs84<{}
                  AND longitude_wgs84>{}
                  AND longitude_wgs84<{}'''.format(latmin, latmax, lonmin, lonmax)).fetchall()
        return self.list_to_dict(tous)

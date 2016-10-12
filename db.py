import sqlite3

class SitesDb(object):
	'''class de gestion de la bdd Sites
	'''
	def __init__(self, path):
		self.db = sqlite3.connect(path)
		self.cursor = self.db.cursor()
		
	def get_all(self):
		tous = self.cursor.execute('''SELECT * FROM SITES''').fetchall()
		liste = []
		for row in tous:
			liste.append(self.row_to_dict(row))
		return liste

	def get_by_id(self, index):
		one = self.cursor.execute('''SELECT * FROM SITES WHERE id_site='''+str(index)).fetchone()
		return self.row_to_dict(one)
		
	def add_site(self, dct):
		self.cursor.execute('''INSERT INTO SITES(nom_fichier_altitudeterrain, tower_height, MF_identifier, wmo_id, longitude_wgs84, ii, site_name, id_radar_model, indicateur_panne, cccc, latitude_wgs84, DPOL_hardware_mode, altitude_site, region_num, wmo_id_bufr_fr) VALUES(:nom_fichier_altitudeterrain, :tower_height, :MF_identifier, :wmo_id, :longitude_wgs84, :ii, :site_name, :id_radar_model, :indicateur_panne, :cccc, :latitude_wgs84, :DPOL_hardware_mode, :altitude_site, :region_num, :wmo_id_bufr_fr)''', dct)
		self.db.commit()
		
	def row_to_dict(self, row):
		d = {}
		for idx, col in enumerate(self.cursor.description):
			d[col[0]] = row[idx]
		return d
        
		

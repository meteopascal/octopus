import sqlite3

class SitesDb(object):
	'''class de gestion de la bdd Sites
	'''
	def __init__(self, path):
		self.db = sqlite3.connect(path)
		self.cursor = self.db.cursor()
		
	def getall(self):
		return self.cursor.execute('''SELECT * FROM SITES''')

	def getone(self, index):
		self.cursor.execute('''SELECT * FROM SITES WHERE wmo_id''')
		
	def add_site(self, dct):
		self.cursor.execute('''INSERT INTO SITES(nom_fichier_altitudeterrain, tower_height, MF_identifier, wmo_id, longitude_wgs84, ii, site_name, id_radar_model, indicateur_panne, cccc, latitude_wgs84, DPOL_hardware_mode, altitude_site, region_num, wmo_id_bufr_fr) VALUES(:nom_fichier_altitudeterrain, :tower_height, :MF_identifier, :wmo_id, :longitude_wgs84, :ii, :site_name, :id_radar_model, :indicateur_panne, :cccc, :latitude_wgs84, :DPOL_hardware_mode, :altitude_site, :region_num, :wmo_id_bufr_fr)''', dct)
		self.db.commit()
        
		

import sqlite3

class MaBdd(object):
	def __init__(self, path):
		self.db = sqlite3.connect(path)
		self.cursor = self.db.cursor()
		
	def getall(self):
		self.cursor.execute('''SELECT * FROM nomdelatable''')
		
	def add(self, dct):
		self.cursor.execute('''INSERT INTO SITES(nom_fichier_altitudeterrain, tower_height, MF_identifier, wmo_id, longitude_wgs84, ii, site_name, id_radar_model, indicateur_panne, cccc, latitude_wgs84, DPOL_hardware_mode, altitude_site, region_num, wmo_id_bufr_fr) VALUES(:nom_fichier_altitudeterrain, :tower_height, :MF_identifier, :wmo_id, :longitude_wgs84, :ii, :site_name, :id_radar_model, :indicateur_panne, :cccc, :latitude_wgs84, :DPOL_hardware_mode, :altitude_site, :region_num, :wmo_id_bufr_fr)''', dct)
		self.db.commit()
        
d = MaBdd("Sites.sqlite")
mondict = {'cccc':'toul','ii':31,'wmo_id':31000,'wmo_id_bufr_fr':31001,'site_name':'toulouse','region_num':12, 'MF_identifier':'toul' , 'latitude_wgs84':44.0,
'longitude_wgs84':1.0 ,'altitude_site':132.0 ,'tower_height':47,'id_radar_model':458,'nom_fichier_altitudeterrain':'toto',
'DPOL_hardware_mode':54,'indicateur_panne':0,'id_radar_model':5} 

#print(', :'.join(mondict.keys()))
d.add(mondict)    
        
 #       id_site, cccc,ii,wmo_id,wmo_id_bufr_fr,site_name,region_num, MF_identifier , latitude_wgs84,
 #       longitude_wgs84 ,altitude_site ,tower_height,id_radar_model,nom_fichier_altitudeterrain,
 #       DPOL_hardware_mode,indicateur_panne,id_radar_model,id_radar_model
		

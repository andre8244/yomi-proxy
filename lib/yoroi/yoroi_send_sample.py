# -*- coding: utf-8 -*-
import json
from flask_json import FlaskJSON, JsonError, json_response, as_json
import requests
from lib.text.convertTuple import convertTuple
from lib.mysql.add_mysql_data import add_mysq_data


client_id = ""
client_secret = ""
grant_type = 'client_credentials'
scope = "/papi/sandbox.submit"
BASE_URL = 'https://users.yoroi.company'


def yoroi_send_sample(hash,filename,fullPath,UPLOAD_FOLDER):
	print("[+]	FUNZIONE INVIO SANDBOX")
	data_token = {
		"client_id": client_id,
		"grant_type": grant_type,
		"client_secret": client_secret,
		"scope": scope
	}
	r = requests.post(BASE_URL+'/pauth/token',
					  data=data_token)
	token_type = json.loads(r.text)
	token = token_type['access_token']

	# Seconda chiamata - SANDBOX
	headers = {"Authorization": "Bearer %s" % token }
	files = {'file' : (filename, open(fullPath, 'rb'))}                                     
	s = requests.post(BASE_URL+'/papi/sandbox',                                             
						headers=headers,                                                    
						files=files)
	print(hash)
	print(s.content)
	if s.status_code == 200:
		#INSERT MYSQL                                                                       
		result = json.loads(s.content)                                                      
		print("[+]	RETRIVE INFORMAZIONI DA YOMI...")
		score = result['score'],                                                            
		score = convertTuple(score)                                                         
		malname = result['file']['filetype']                                                
		malname = convertTuple(malname)                                                     
		scan_id = result['_id']
		if score == None:
			msg = "Analisi in corso."
			return json_response(ERRORE=msg)
		else:
			return add_mysq_data(scan_id,hash,malname,score)
	else:
		return json_response(ERRORE=s.status_code)




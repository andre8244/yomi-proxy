# -*- coding: utf-8 -*-
import json
from flask_json import FlaskJSON, JsonError, json_response, as_json
import requests
from lib.text.convertTuple import convertTuple


client_id = ""
client_secret = ""
grant_type = 'client_credentials'
scope = "/papi/sandbox.submit"
BASE_URL = 'https://users.yoroi.company'


def yoroi_send_sample(filename,fullPath):
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
	if s.status_code == 200:
		result = json.loads(s.content)                                                      
		score = result['score'],                                                            
		score = convertTuple(score)                                                         
		malname = result['file']['filetype']
		malname = convertTuple(malname) 
		scan_id = result['_id']
		if score == None:
			return json_response(scan_id=-1, hash='', malware='', score=-1, status_=404)
		else:
			return json_response(scan_id=scan_id, hash='', malware=malname, score=score, status_=200)
	else:
		return json_response(scan_id=-1, hash='', malware='', score=-1, status=s.status_code)




# -*- coding: utf-8 -*-
import json
from flask_json import FlaskJSON, JsonError, json_response, as_json
import requests
from flask import current_app as app
from lib.text.convertTuple import convertTuple


def yoroi_send_sample(filename,fullPath):
	data_token = {
		"client_id": app.config["YOROI_CLIENT_ID"],
		"grant_type": "client_credentials",
		"client_secret": app.config["YOROI_CLIENT_SECRET"],
		"scope": "/papi/sandbox.submit"
	}

	r = requests.post(app.config["BASE_URL"]+'/pauth/token',
					  data=data_token)
	token_type = json.loads(r.text)
	token = token_type['access_token']

	headers = {"Authorization": "Bearer %s" % token }
	files = {'file' : (filename, open(fullPath, 'rb'))}                                     
	s = requests.post(app.config["BASE_URL"]+'/papi/sandbox',                                             
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




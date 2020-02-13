# -*- coding: utf-8 -*-
import json
from flask_json import FlaskJSON, JsonError, json_response, as_json
import requests
from flask import current_app as app


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

		if result['score'] is None or result['_id'] == "":
			# submission accepted, return work in progress status
			return json_response(scan_id=-1, hash='', malware='', score=-1, status_=202)
		else:
			# we already have a score, just return it
			return json_response(scan_id=result['_id'], hash=result['file']['hash']['sha256'], malware=result['threat']['name'], score=result['score'], status_=200)
	else:
		# upstream error
		return json_response(scan_id=-1, hash='', malware='', score=-1, status=s.status_code)




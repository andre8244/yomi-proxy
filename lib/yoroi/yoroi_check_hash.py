# -*- coding: utf-8 -*-
from flask_json import FlaskJSON, JsonError, json_response, as_json
import requests
from flask import request
from flask import current_app as app


def yoroi_check_sha256(hash):
	data_token = {
		"client_id": app.config["YOROI_CLIENT_ID"],
		"grant_type": "client_credentials",
		"client_secret": app.config["YOROI_CLIENT_SECRET"],
		"scope": "/papi/sandbox.lookup"
	}
	r = requests.post(app.config["BASE_URL"]+'/pauth/token', data=data_token)
	response = r.json()
	headers = {"Authorization": "Bearer %s" % response['access_token'], 'Content-type': 'application/json'}
	s = requests.get(app.config["BASE_URL"]+'/papi/sandbox/hash/'+hash, headers=headers)
	try:
		r = s.json()
	except:
		return json_response(score=-1, malware='', yoroi_sha256='', yomi_id=-1, status_=s.status_code)
	if s.status_code == 200:
		if not r:
			return  json_response(score=-1, malware='', yoroi_sha256='', yomi_id=-1, status_=404)
		r = r[0]
		return  json_response(score=r['score'], malware=r['threat']['name'], yoroi_sha256=r['file']['hash']['sha256'], yomi_id=0)
	else:
		return json_response(score=-1, malware='', yoroi_sha256='', yomi_id=-1, status_=s.status_code)

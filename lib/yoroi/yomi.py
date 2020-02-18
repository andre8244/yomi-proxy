# -*- coding: utf-8 -*-
from flask_json import FlaskJSON, JsonError, json_response
import requests
import json
from flask import request
from flask import current_app as app

bearer = { '/papi/sandbox.lookup' : '', '/papi/sandbox.submit' : '' }

def authenticate(scope, refresh = False):
	if bearer[scope] and not refresh:
		return bearer[scope]
	else:
		data_token = {
			"client_id": app.config["YOROI_CLIENT_ID"],
			"grant_type": "client_credentials",
			"client_secret": app.config["YOROI_CLIENT_SECRET"],
			"scope": scope
		}
		r = requests.post(app.config["BASE_URL"]+'/pauth/token', data=json.dumps(data_token), headers={'Content-type': 'application/json'})
		if r.status_code != 200:
			bearer[scope] = ''
		else:
			try:
				response = r.json()
				bearer[scope] = response['access_token']
			except:
				bearer[scope] = ''
		return bearer[scope]


def yoroi_check_sha256(hash):
	bearer = authenticate('/papi/sandbox.lookup')
	headers = {"Authorization": "Bearer %s" % bearer, 'Content-type': 'application/json'}
	s = requests.get(app.config["BASE_URL"]+'/papi/sandbox/hash/'+hash, headers=headers)

        # refresh token if expired
	if s.status_code == 401:
		bearer = authenticate('/papi/sandbox.lookup', True)
		headers = {"Authorization": "Bearer %s" % bearer, 'Content-type': 'application/json'}
		s = requests.get(app.config["BASE_URL"]+'/papi/sandbox/hash/'+hash, headers=headers)
	
	if s.status_code == 200:
		try:
			r = s.json()
		except:
			return json_response(score=-1, malware='', yoroi_sha256='', yomi_id=-1, status_=500)

		if not r:
			return  json_response(score=-1, malware='', yoroi_sha256='', yomi_id=-1, status_=404)
		r = r[0]
		score = r['score'] if r['score'] else -1
		return  json_response(score=r['score'], malware=r['threat']['name'], yoroi_sha256=r['file']['hash']['sha256'], yomi_id=0)
	else:
		return json_response(score=-1, malware='', yoroi_sha256='', yomi_id=-1, status_=s.status_code)

def yoroi_send_sample(filename,fullPath):
	bearer = authenticate('/papi/sandbox.submit')
	headers = {"Authorization": "Bearer %s" % bearer}
	files = {'file' : (filename, open(fullPath, 'rb'))}                                     
	s = requests.post(app.config["BASE_URL"]+'/papi/sandbox', headers=headers, files=files)

        # refresh token if expired
	if s.status_code == 401:
		bearer = authenticate('/papi/sandbox.submit', True)
		headers = {"Authorization": "Bearer %s" % bearer}
		s = requests.post(app.config["BASE_URL"]+'/papi/sandbox', headers=headers, files=files)
	
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




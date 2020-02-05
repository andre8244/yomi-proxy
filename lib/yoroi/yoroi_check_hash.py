# -*- coding: utf-8 -*-
import json
from flask_json import FlaskJSON, JsonError, json_response, as_json
import requests
from flask import request
from lib.text.convertTuple import convertTuple
from lib.mysql.add_mysql_data import add_mysq_data_min


client_id = ""
client_secret = ""
grant_type = 'client_credentials'
scope = "/papi/sandbox.lookup"
BASE_URL = 'https://users.yoroi.company'



def yoroi_check_sha256(hash):
	print("[+]	FUNZIONE GET SANDBOX TOKEN")
	data_token = {
		"client_id": client_id,
		"grant_type": grant_type,
		"client_secret": client_secret,
		"scope": scope
	}
	r = requests.post(BASE_URL+'/pauth/token',
					  data=data_token)
	token = json.loads(r.content)
	token = token['access_token']
	#seconda richiesta
	headers = {"Authorization": "Bearer %s" % token }
	s = requests.get(BASE_URL+'/papi/sandbox/hash/'+hash, headers=headers)
	result = json.loads(s.content)
	if s.status_code == 200:
		print("[+]	RETRIVE INFORMAZIONI DA YOMI...")
		for r in result:
			hash = r['file']['hash']['sha256'],
			hash = convertTuple(hash)
			score = r['score'],
			score = convertTuple(score)
			return add_mysq_data_min(hash, score)
	elif s.status_code == 400:
		hack = "Are you try to hack me? "
		ip = request.remote_addr
		message= "Mail sent to system administrator."
		return json_response(ERRORE=hack, IP=ip)
	else:
		return json_response(ERRORE=s.status_code)

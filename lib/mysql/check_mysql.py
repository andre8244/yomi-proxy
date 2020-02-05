import pymysql
import json
from flask_json import FlaskJSON, JsonError, json_response, as_json
import os, sys
from lib.yoroi.yoroi_send_sample import yoroi_send_sample
from lib.text.convertTuple import convertTuple

db = pymysql.connect(host="192.168.5.157",
                     user="yomi_user",
                     passwd="yomi_password",
                     db="nethesis_sandbox")


def check_mysql(hash, filename, fullPath, file, UPLOAD_FOLDER):
	print("[+]	FUNZIONE CHECK MYSQL")
	cursor = db.cursor()
	result = cursor.execute("SELECT hash, score FROM ( SELECT sandbox.score, sandbox.hash FROM sandbox UNION ALL SELECT sandbox_min.score, sandbox_min.hash FROM sandbox_min)  sandbox WHERE hash = '%s'" % (hash))
	result = cursor.fetchone()
	if result == None:
		# valutare codice HTTP 102 Processing   26/1/20
		print("[!]	HASH NON TROVATO NELLE TABELLE. INVIO A YOMI.")
		return yoroi_send_sample(hash,filename,fullPath,UPLOAD_FOLDER)
	else:
		hasha = result[0],
		score = result[1]
		print("[+]	HASH RILEVATO.")
		return json_response(score=score, yoroi_sha256=hasha, status_=200)



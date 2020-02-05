# -*- coding: utf-8 -*-
import pymysql
from flask_json import FlaskJSON, JsonError, json_response, as_json
from lib.yoroi.yoroi_check_hash import yoroi_check_sha256

db = pymysql.connect(host="192.168.5.157",
                     user="yomi_user",            
                     passwd="yomi_password",      
                     db="nethesis_sandbox")  

def check_hash(hash):
    print("[+]	FUNZIONE CHECK HASK")
    cursor = db.cursor()
    sandbox = cursor.execute("SELECT hash, score FROM ( SELECT sandbox.score, sandbox.hash FROM sandbox UNION ALL SELECT sandbox_min.score, sandbox_min.hash FROM sandbox_min)  sandbox WHERE hash = '%s'" % (hash))
    result = cursor.fetchone()
    if result == None:
        # valutare codice HTTP 102 Processing   26/1/20
        print("[!]	HASH NON TROVATO NELLA TABELLE. INVIO A YOMI.")
        return yoroi_check_sha256(hash)
    else:
        hasha = result[0],
        score = result[1]
        print("[+]	HASH RILEVATO.")
        return json_response(score=score, yoroi_sha256=hasha, status_=200)

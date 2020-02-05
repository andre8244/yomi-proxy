# -*- coding: utf-8 -*-
import pymysql
from flask_json import FlaskJSON, JsonError, json_response, as_json

db = pymysql.connect(host="192.168.5.157",
                     user="yomi_user",            
                     passwd="yomi_password",      
                     db="nethesis_sandbox")       


def add_mysq_data(scan_id,hash,malname,score):
    print("[!]  SCRIVO NUOVO HASH NELLA TABELLA SANDBOX.")
    cursor = db.cursor()
    cursor.execute("INSERT INTO sandbox (scan_id, hash, malname, score) VALUES ('%s','%s','%s',%s)" % (scan_id, hash, malname, score))
    db.commit()
    print("Dati inseriti correttamente.")
    return json_response(score=score, malware_name=malname, yoroi_sha256=hash, yomi_id=scan_id,_status=200)


def add_mysq_data_min(hash,score):
    print("[!]  SCRIVO NUOVO HASH NELLA TABELLA SANDBOX_MIN.")
    cursor = db.cursor()
    cursor.execute("INSERT INTO sandbox_min (hash, score) VALUES ('%s','%s')" % (hash, score))
    db.commit()
    print("Dati inseriti correttamente.")
    return json_response(score=score, yoroi_sha256=hash,_status=200)

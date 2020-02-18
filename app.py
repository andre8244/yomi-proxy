# -*- coding: utf-8 -*-
from flask import Flask, redirect, url_for, request, render_template, flash, abort, request
import sys, os, time, json, base64, tempfile, hashlib
from flask_json import FlaskJSON, JsonError, json_response, as_json

from lib.yoroi.yomi import yoroi_send_sample, yoroi_check_sha256

#config
app = Flask(__name__)
FlaskJSON(app)

app.secret_key =  os.environ.get("SECRET_KEY") if  os.environ.get("SECRET_KEY")  else "weak_secret"
app.config['UPLOAD_FOLDER'] = os.environ.get("UPLOAD_FOLDER") if os.environ.get("UPLOAD_FOLDER")  else  "/tmp/yomi"
app.config['YOROI_CLIENT_ID'] = os.environ.get("YOROI_CLIENT_ID") if  os.environ.get("YOROI_CLIENT_ID") else ""
app.config['YOROI_CLIENT_SECRET'] = os.environ.get("YOROI_CLIENT_SECRET") if  os.environ.get("YOROI_CLIENT_SECRET") else ""
app.config['BASE_URL'] = "https://users.yoroi.company"



@app.route('/', methods=['GET'])
def index():
    return '''
         <html>
         <h3> >_ NethSandbox</h3>
         </html>  
    '''

#entry point
@app.route('/submit', methods=['POST'])
def uplod_base64():
    content = request.get_json()
    d = base64.decodestring(content['data'].encode())

    # temporary file name is sha256 hash of the content
    sha = hashlib.sha256(d).hexdigest()
    name = os.path.join(app.config['UPLOAD_FOLDER'],sha)
    tmp = open(name,"wb")
    tmp.write(d)
    tmp.close()

    return yoroi_send_sample('upload', name)


@app.route('/hash/<string:hash>', methods=['GET'])
def check(hash):
    return yoroi_check_sha256(hash)

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")


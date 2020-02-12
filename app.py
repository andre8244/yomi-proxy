# -*- coding: utf-8 -*-
from flask import Flask, redirect, url_for, request, render_template, flash, abort, request
from werkzeug.utils import secure_filename
import hashlib
import sys, os, time, json
import base64, tempfile
from flask_json import FlaskJSON, JsonError, json_response, as_json
#lib nostre
from lib.text.convertTuple import convertTuple
from lib.yoroi.yoroi_send_sample import yoroi_send_sample
from lib.yoroi.yoroi_check_hash import yoroi_check_sha256

#config
app = Flask(__name__)
FlaskJSON(app)
app.secret_key = "ui7rie5oThee7xa1yahxu2Boh5Riesei2PosieyiHaijahxahngidoogh9ceequ1"
app.config['JSON_ADD_STATUS'] = False
UPLOAD_FOLDER = '/tmp/yomi'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER




def allowed_file(filename):
	return True
    #return '.' in filename and \
           #filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION


@app.route('/', methods=['GET'])
def index():
    return '''
         <html>
         <h3> >_ NethSandbox</h3>
         </html>  
    '''

#entry point
@app.route('/detection', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return abort(404)
        file = request.files['file']
        if file.filename == '':
            return abort(404)
        if file and allowed_file(file.filename):
            hash = hashlib.sha256(file.read()).hexdigest()
            filename = secure_filename(file.filename)
            fullPath = os.path.join(UPLOAD_FOLDER, filename)
            print("[*]  CHECK PRESENZA FILE.")
            if os.path.isfile(fullPath):
                print("[+]  FILE PRESENTE.")
                return check_mysql(hash, filename, fullPath, file, UPLOAD_FOLDER)
            else:
                print("[!]  FILE NON PRESNTE.")
                file.stream.seek(0)
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                return check_mysql(hash, filename, fullPath, file, UPLOAD_FOLDER)

    else:
        return '''                                                              
			<!doctype html>                                                     
    		<form method=post enctype=multipart/form-data>                      
    		<input type=file name=file>                                         
    		<input type=submit value=Upload>                                    
    		</form>                                                             
    		'''

@app.route('/submit', methods=['POST'])
def uplod_base64():
    content = request.get_json()
    # print("content=%s" % content['data']);
    d = base64.decodestring(content['data'].encode())
    fd, name = tempfile.mkstemp(dir=UPLOAD_FOLDER)
    print("filename=%s" %name)
    with os.fdopen(fd, "wb") as tmp:
            tmp.write(d)
            tmp.close()
    return yoroi_send_sample('upload', name)


@app.route('/hash/<string:hash>', methods=['GET'])
def check(hash):
    return yoroi_check_sha256(hash)

if __name__ == '__main__':
    #app.run(ssl_context=('cert.pem', 'key.pem'),debug=True,host="0.0.0.0")
    app.run(debug=True,host="0.0.0.0")


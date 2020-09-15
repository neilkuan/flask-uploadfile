# -*- coding: utf-8 -*-
import os
from datetime import datetime, timezone, timedelta
from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import json
import platform
from functools import wraps
import secrets


cwd = os.getcwd()
URL=os.getenv('URL')
UPLOAD_FOLDER = cwd + '/pic/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip','tar'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# add secret key , example output, secret_key = 000d88cd9d90036ebdd237eb6b0db000
secret_key = secrets.token_hex(16)
app.secret_key = secret_key

# LET USER LOGIN FIRST
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)       
        flash('You need to login first.')
        return redirect(url_for('login'))
    return wrap

# get file create time .
def creation_date(path_to_file):
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)   
    stat = os.stat(path_to_file)
    try:
        return stat.st_birthtime
    except AttributeError:
        # We're probably on Linux. No easy way to get creation dates here,
        # so we'll settle for when its content was last modified.
        return stat.st_mtime

# print(datetime.fromtimestamp(creation_date('./pic/.gitkeep')).isoformat(timespec="seconds"))

# what time is it ??
def what_time_is():
    tz = timezone(timedelta(hours=+8))
    datetime.now(tz).isoformat()
    time = datetime.now(tz).isoformat(timespec="seconds")
    return  time

# get file size
def get_file_size(path_to_file):
    result = None
    try:
        size = os.path.getsize(path_to_file)
        if size <= 1024:
            result = str(size) + " bytes "
        if size > 1024 and 1024*1024 >= size:
            result = str(round(size/1024, 2)) + " KB "
        if size > 1024*1024 and 1024*1024*1024 >= size:
            result = str(round(size/(1024*1024),2)) + " MB "
    finally:
        if result is None:
            result = 'None'
    return result

# 解析檔案名稱
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def download_file(name):
    file_create_time = datetime.fromtimestamp(creation_date(cwd + "/pic/" + name)).isoformat(timespec="seconds")
    file_size = get_file_size(cwd + "/pic/" + name)
    return '''<div style=inline>
    <p>{file_create_time}</p>
    <p>{file_size}</p>
    <a href="./downloadfile/{name}" download="{name}">{name}</a>
    </div>'''.format(name=name , file_create_time=file_create_time, file_size=file_size)

# login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            flash('Your already login !!!')
            return redirect(url_for('index_page'))
            
    return render_template('login.html', error=error)

@app.route('/ping')
def test():
    return jsonify({"message": "pong!!!" })

# show table .
@app.route('/show', methods=['GET', 'POST'])
@login_required
def show():
    listfile='''<div style=inline><p> File Create Time </p>
    <p></p><p></p><p></p><p></p>
    <p> Size </p>
    <p></p><p></p><p></p><p></p>
    <p> Name </p></div>'''
    pic_file_list = os.listdir( cwd + '/pic' )
    for i in pic_file_list: 
        listfile += download_file(i)+'<br>'
    return render_template('show.html', table=listfile)
    
#Download file
@app.route('/downloadfile/<filename>', methods=['GET'])
def return_file(filename):
    return send_from_directory(directory='pic', filename=filename, as_attachment=True)

#Delete file
@app.route('/deletefile/<filename>', methods=['DELETE'])
def delete_file(filename):
    os.remove(cwd + '/pic/' + filename)
    return {"status": "deleted"}
    
# Upload file
@app.route('/uploadfile', methods=['POST'])
def upload_file():
    res = redirect(url_for('index_page'))
    try:
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            res = redirect(url_for('index_page'))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # 儲存在 app 本地端
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            successres = str("Date " + what_time_is() + " 上傳 " + filename + " 成功")

            res = render_template('uploadPage.html', successres=successres)
        if not allowed_file(file.filename):
            flash('Not Allow File type , please upload type in txt, pdf, png, jpg, jpeg, gif, zip,tar')
            res = redirect(url_for('index_page'))
    finally:
        return res

# 建立上傳網址
@app.route('/', methods=['GET', 'POST'])
@login_required
def index_page():
    if request.form.get('show') == "show":
        return redirect(url_for('show'))

    if request.form.get('logout') == "logout":
        return redirect(url_for('logout'))

    return render_template('index.html') 

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template

# define logout 
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You already logout !!!')
    return redirect(url_for('welcome'))

# start the server
if __name__ == '__main__':
    app.run(host=URL,port=8080)
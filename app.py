import os
from datetime import datetime, timezone, timedelta
from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import json
import platform
from functools import wraps
import secrets


cwd = os.getcwd()

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
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

def format_table():
    from flask_table import Table, Col
    pic_file_list = os.listdir( cwd + '/pic' )
    class ItemTable(Table):
        name = Col('Name')
        download_link = Col('Download Link')
    
    # Get some objects
    class Item(object):
        def __init__(self, name, download_link):
            self.name = name
            self.download_link = download_link
    items = []
    for i in pic_file_list: 
        items.append(Item(str(i),'http://nexus-registry.cathayins-dev.com/downloadfile/'+ str(i)))
    table = ItemTable(items)
    
    return table.__html__()

# get file create time .
def creation_date(path_to_file):
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
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
    try:
        size = os.path.getsize(path_to_file)
        if size <= 1024:
            return str(size) + " bytes "
        elif size > 1024 and 1024*1024 >= size:
            return str(round(size/1024, 2)) + " KB "
        elif size > 1024*1024 and 1024*1024*1024 >= size:
            return str(round(size/(1024*1024),2)) + " MB "
        else:
            return "None"
    except:
        return "have nothing wrong !!!"

# 解析檔案名稱
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# format josn .
def pp_json(json_thing, sort=True, indents=4):
   if type(json_thing) is str:
       return json.dumps(json.loads(json_thing), sort_keys=sort, indent=indents)
   else:
       return  json.dumps(json_thing, sort_keys=sort, indent=indents)
   return None

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

# Upload file
@app.route('/uploadfile', methods=['POST'])
def upload_file():
    try:
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        elif file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # 儲存在 app 本地端
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            successres = str("Date " + what_time_is() + " 上傳 " + filename + " 成功")

            return render_template('uploadPage.html', successres=successres)
    except:
        return render_template('index.html')

# 建立上傳網址
@app.route('/', methods=['GET', 'POST'])
@login_required
def index_page():
    if request.form.get('show') == "show":
        return redirect(url_for('show'))

    elif request.form.get('logout') == "logout":
        return redirect(url_for('logout'))

    else:
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
    app.run(host='0.0.0.0',port=8080)
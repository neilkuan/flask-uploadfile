import os
from datetime import datetime, timezone, timedelta
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import send_from_directory , jsonify , send_file ,render_template
import json


tz = timezone(timedelta(hours=+8))
UPLOAD_FOLDER = './pic/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip','tar'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def format_table():
    from flask_table import Table, Col
    pic_file_list = os.listdir( './pic' )
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
    return '''<a href="./downloadfile/{name}" download="{name}">
              {name}</a>'''.format(name=name)

def head_two(name):
    return "<h2> {name} </h2>".format(name=name)

@app.route('/ping')
def test():
    return jsonify({"message": "pong!!!" })

# show table .
@app.route('/show', methods=['GET', 'POST'])
def show():
    listfile=''
    pic_file_list = os.listdir( './pic' )
    for i in pic_file_list: 
        listfile += '<br>'+download_file(i)
    return render_template('show.html', table=listfile)
    

#Download file
@app.route('/downloadfile/<filename>', methods=['GET'])
def return_file(filename):
    return send_from_directory(directory='pic', filename=filename, as_attachment=True)


# 建立上傳網址
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    from flask import render_template
    if request.method == 'POST':

        if request.form.get('Upload') == "Upload":
            try:
                file = request.files['file']
                # if user does not select file, browser also
                # submit an empty part without filename
                if file.filename == '':
                    flash('No selected file')
                    return redirect(request.url)
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    # 儲存在 app 本地端
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
                    datetime.now(tz).isoformat()
                    time = datetime.now(tz).isoformat(timespec="seconds")
    
                    successres = str("Date " + time + " 上傳 " + filename + " 成功")
    
                    return render_template('uploadPage.html', successres=successres)
            except:
                return render_template('index.html')

        if request.form.get('back') == "back":
            return render_template('index.html')

        try: 
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # 儲存在 app 本地端
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                datetime.now(tz).isoformat()
                time = datetime.now(tz).isoformat(timespec="seconds")
                
                successres = str("Date " + time + " 上傳 " + filename + " 成功")
            
                return render_template('uploadPage.html', successres=successres)
        except:
            pass
        
        

    if request.method == 'GET':
        return render_template('index.html')        
    else:
        return "have something wrong !!!"
    return render_template('index.html') 


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080)
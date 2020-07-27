from flask_table import Table, Col, LinkCol
from flask import Flask
import os 
from flask import send_from_directory , jsonify , send_file ,render_template

'''A example for creating a simple table within a working Flask app.
Our table has just two columns, one of which shows the name and is a
link to the item's page. The other shows the description.
'''

def download_file(name):
    return '''<a href="./downloadfile/{name}" download="{name}">
              {name}</a>'''.format(name=name)

app = Flask(__name__)


def format_table():
    pic_file_list = os.listdir( '../pic' )
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
        items.append(Item(str(i), download_file(str(i))))
    table = ItemTable(items,border="1")
    
    return (table.__html__())


@app.route('/')
def index():
    listfile=''
    pic_file_list = os.listdir( '../pic' )
    for i in pic_file_list: 
        listfile += '<br>'+download_file(i)
    return render_template('show.html', table=listfile)
    #return table


if __name__ == '__main__':
    app.run()
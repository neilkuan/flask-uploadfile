import os

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


from flask import Flask, render_template, request, session
from datetime import date, datetime, timedelta
from pymongo import MongoClient
import io
import csv
import datetime
from PIL import Image
from StringIO import StringIO
import mysql.connector
import time




from azure.storage.blob import BlockBlobService
from azure.storage.blob import PublicAccess
from azure.storage.blob import ContentSettings

#cnx = mysql.connector.connect(user={battula@battula}, password={Sharingan123!}, host={battula.mysql.database.azure.com}, port={3306}, database={quickstartdb}[, ssl_ca={BaltimoreCyberTrustRoot.crt.pem}, ssl_verify_cert=true])

try:
    conn=mysql.connector.connect(user='davidlevine@davidlevine',
                                 password='Sharingan123!',
                                 database='quickstartdb',
                                 host='davidlevine.mysql.database.azure.com',
                                 ssl_ca='/Users/charith_gunuganti/Desktop/BaltimoreCyberTrustRoot.crt.pem',
                                 ssl_verify_cert='true' )


except mysql.connector.Error as err:
    print(err)

app = Flask(__name__)

block_blob_service = BlockBlobService(account_name='abc23', account_key='SIoFvnyWW1S38GQJW92LyP29B2DZY5h4cibV/fROMZ3LnTEITuaQ+5ed/FYUrqy2DRKULJs0ALpyXrD7lIb0ig==')
block_blob_service.create_container('mycontainer', public_access=PublicAccess.Container)


@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/upload',methods=['POST'])
def upload():
    f = request.files['file']
    tit = request.form['title']
    file_name = f.filename
    img_name = file_name.split('.')
    f.save('/Users/charith_gunuganti/Desktop/abcd' + file_name)
    location = '/Users/charith_gunuganti/Desktop/abcd' + file_name
    block_blob_service.create_blob_from_path('mycontainer', img_name[0], location,
                                             content_settings=ContentSettings(content_type='image/jpg'))
                                             cursor = conn.cursor()
                                             add_img = ("INSERT INTO imgstore "
                                                        "(imgname, title, datetime, likes) "
                                                        "VALUES (%(imgname)s, %(title)s, %(datetime)s, %(likes)s)")
                                             data_img = {
                                                 'imgname': img_name[0],
                                                     'title': tit,
                                                         'datetime': time.strftime('%Y-%m-%d %H:%M:%S'),
                                                             'likes': 0,
                                                         }

cursor.execute(add_img, data_img)
    conn.commit()
    cursor.close()
    
    return render_template("home.html")


@app.route('/disp',methods=['POST'])
def disp():
    iname=request.form['iname']
    generator = block_blob_service.list_blobs('mycontainer')
    for blob in generator:
        if blob.name == iname:
            obj1 = block_blob_service.make_blob_url('mycontainer', blob.name, protocol='https')
    return render_template('home.html',user_image=obj1)


@app.route('/dispall',methods=['POST'])
def dispall():
    cursor = conn.cursor()
    imgname = []
    imgtitle = []
    likes = []
    que_img = ("SELECT * FROM imgstore ")
    cursor.execute(que_img)
    c=cursor.fetchall()
    return render_template('home.html', data=c)



def findImage(containerName, imageName):
    return block_blob_service.get_blob_to_bytes(
                                                containerName,
                                                imageName,
                                                max_connections=1).content;




if __name__ == '__main__':
    app.run()
    conn.close()

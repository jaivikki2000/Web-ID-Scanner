from flask import Flask
from flask import request,redirect,render_template,url_for
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL
import MySQLdb.cursors
import os
import pytesseract
from PIL import ImageFilter
from PIL import Image
import sys
pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\Tesseract.exe'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './media'
app.config['MYSQL_HOST'] = 'remotemysql.com'
app.config['MYSQL_USER'] = 'Q8Ev2QhHEl'
app.config['MYSQL_PASSWORD'] = '3a12SuiAuA'
app.config['MYSQL_DB'] = 'Q8Ev2QhHEl'
mysql = MySQL(app)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submitImage/',methods=['POST',])
def submitImage():
    image = request.files['ocrImage']
    text = ''
    filename = secure_filename(image.filename)
    image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    img = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    text = pytesseract.image_to_data(img)
    cursor = mysql.connection.cursor()
    cursor.execute('INSERT INTO newtable VALUES(% s)',(text,))
    mysql.connection.commit()
    msg = "you have sucessfully got registered"
    f = open(os.path.join(app.config['UPLOAD_FOLDER'], filename)+'.txt','w')
    f.write(text)
    f.close()
    return render_template('textFile.html',text=text,msg=msg,filename=f)


if __name__ == '__main__':
   app.run(host="0.0.0.0", port=5000, debug=True)

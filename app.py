import os
from os.path import join, dirname
from dotenv import load_dotenv

from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)

db = client[DB_NAME]

app= Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    articles = list(db.diary.find({},{'_id':False}))
    return jsonify({'articles' : articles})

@app.route('/diary', methods=['POST'])
def save_diary():
    title_receive = request.form.get('title_give')
    content_receive= request.form.get('content_give')

    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    if 'file_give' in request.files :
        file = request.files["file_give"]
        extension = file.filename.split('.')[-1]
        file_name = file.filename.split('.')[0]
        newFileName= f'{file_name}({mytime}).{extension}'
        file.save(f'static/{newFileName}')
    else : 
        newFileName = 0

    if 'profile_give' in request.files :
        profile = request.files["profile_give"]
        extension = profile.filename.split('.')[-1]
        profile_name = profile.filename.split('.')[0]
        newProfileName= f'{profile_name}({mytime}).{extension}'
        profile.save(f'static/{newProfileName}')
    else :
        newProfileName = 0

    doc = {
        'file' : newFileName,
        'profile': newProfileName,
        'title': title_receive,
        'content' : content_receive
    }
    db.diary.insert_one(doc)
    return jsonify({'message' : 'data was saved!!!'})


if __name__== '__main__':
    app.run('0.0.0.0', port=5000, debug=True)


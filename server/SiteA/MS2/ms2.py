from flask import Flask, request, jsonify
import os
from peewee import *
from datetime import datetime
import requests

db_path = os.path.join(os.path.dirname(__file__), '..', 'db_a.db')
db = SqliteDatabase(db_path)

class BaseModel(Model):
    class Meta:
        database = db

class Mahasiswa(BaseModel):
    nama = TextField()
    sem = TextField()
    timestamp = DateTimeField(default=datetime.now)

def create_tables():
    db.connect()
    db.create_tables([Mahasiswa])

app = Flask(__name__)

@app.route('/')
def home():
    return "Server MS2 ready"

@app.route('/ms2', methods=['POST'])
def add_data_ms2():
    data = request.get_json()
    nama = data.get('nama')
    sem = data.get('sem')
    source = data.get('source', None)

    
    mahasiswa = Mahasiswa.create(nama=nama, sem=sem)

    if source != 'ms3':
        forward_to_ms3(nama, sem, source)

    return jsonify({"message": "Data processed by MS2 and forwarded to MS3 if necessary"}), 200

@app.route('/ms2/data', methods=['GET'])
def get_data_ms2():
    mahasiswa_data = Mahasiswa.select()    
    data = [
        {
            'id': m.id,
            'nama': m.nama,
            'sem': m.sem,
            'timestamp': m.timestamp.strftime('%d/%m/%y %H:%M:%S')  
        } 
        for m in mahasiswa_data
    ]
    
    return jsonify(data)

def forward_to_ms3(nama, sem, source):
    url_ms3 = "http://localhost:5053/ms3"
    data = {'nama': nama, 'sem': sem, 'source': 'ms2'}  
    response = requests.post(url_ms3, json=data)
    return response

if __name__ == '__main__':
    
    create_tables()
    app.run(port=5052)

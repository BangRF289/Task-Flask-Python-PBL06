from flask import Flask, request, jsonify
import requests
import os
from peewee import *
from datetime import datetime

db_path = os.path.join(os.path.dirname(__file__), '..', 'db_b.db')
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
    return "Server MS3 ready"

@app.route('/ms3', methods=['POST'])
def add_data_ms3():
    data = request.get_json()
    nama = data.get('nama')
    sem = data.get('sem')
    source = data.get('source', None)

    mahasiswa = Mahasiswa.create(nama=nama, sem=sem)

    if source != 'ms2':
        forward_to_ms2(nama, sem, source)

    return jsonify({"message": "Data processed by MS3 and forwarded to MS2 if necessary"}), 200

@app.route('/ms3/data', methods=['GET'])
def get_data_ms3():
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


def forward_to_ms2(nama, sem, source):
    url_ms2 = "http://localhost:5052/ms2"
    data = {'nama': nama, 'sem': sem, 'source': 'ms3'}  
    response = requests.post(url_ms2, json=data)
    return response

if __name__ == '__main__':

    create_tables()
    app.run(port=5053)

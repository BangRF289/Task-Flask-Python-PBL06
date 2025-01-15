from flask import Flask, request, jsonify
import os
from peewee import *
from datetime import datetime

app = Flask(__name__)

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


def save_to_db_a(nama, sem):
    with db.connection_context():  
        Mahasiswa.create(nama=nama, sem=sem)

@app.route('/')
def home():
    return "Server MS1 ready"

@app.route('/ms1', methods=['POST'])
def add_data_ms1():
    data = request.get_json()
    nama = data.get('nama')
    sem = data.get('sem')

    save_to_db_a(nama, sem)

    return jsonify({"message": "Data added to MS1 (db_a)"}), 200

@app.route('/ms1/data', methods=['GET'])
def get_data_ms1():
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

if __name__ == '__main__':
    
    create_tables()
    app.run(port=5051)

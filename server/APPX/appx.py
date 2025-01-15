from flask import Flask, render_template, request, redirect, url_for
import requests
import os

app = Flask(__name__, template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '../../client/templates')))

def get_data_from_ms1():
    url_ms1 = "http://localhost:5051/ms1/data"
    response = requests.get(url_ms1)
    return response.json() if response.status_code == 200 else []

def get_data_from_ms3():
    url_ms3 = "http://localhost:5053/ms3/data"
    response = requests.get(url_ms3)
    return response.json() if response.status_code == 200 else []

@app.route('/')
def display_data():
    db_a_data = get_data_from_ms1()
    db_b_data = get_data_from_ms3()

    return render_template('index.html', db_a_data=db_a_data, db_b_data=db_b_data)

@app.route('/ms1', methods=['GET', 'POST'])
def ms1_form():
    if request.method == 'POST':
        nama = request.form['nama']
        sem = request.form['sem']

        url_ms1 = "http://localhost:5051/ms1"
        data = {'nama': nama, 'sem': sem}
        response = requests.post(url_ms1, json=data)

        if response.status_code == 200:
            return redirect(url_for('display_data'))
        else:
            return "Error adding data to MS1", 500

    return render_template('ms1.html')

@app.route('/ms2', methods=['GET', 'POST'])
def ms2_form():
    if request.method == 'POST':
        nama = request.form['nama']
        sem = request.form['sem']

        url_ms2 = "http://localhost:5052/ms2"
        data = {'nama': nama, 'sem': sem}
        response = requests.post(url_ms2, json=data)

        if response.status_code == 200:
            return redirect(url_for('display_data'))
        else:
            return "Error adding data to MS2", 500

    return render_template('ms2.html')

@app.route('/ms3', methods=['GET', 'POST'])
def ms3_form():
    if request.method == 'POST':
        nama = request.form['nama']
        sem = request.form['sem']

        url_ms3 = "http://localhost:5053/ms3"
        data = {'nama': nama, 'sem': sem}
        response = requests.post(url_ms3, json=data)

        if response.status_code == 200:
            return redirect(url_for('display_data'))
        else:
            return "Error adding data to MS3", 500

    return render_template('ms3.html')

if __name__ == '__main__':
    app.run(port=5000, debug=True)

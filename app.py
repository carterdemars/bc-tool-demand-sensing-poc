import csv
import itertools
import logging
import os
import requests
from utils.utils import read_data
from flask import Flask, flash, redirect, render_template, request, send_from_directory, send_file, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

# app.config['DEBUG'] = True # enables debugging mode for development
app.config['UPLOAD_FOLDER'] = 'data/'


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    # verify that the post request has the file
    if 'file' not in request.files:
        flash('No file was selected')
        return redirect(url_for('home'))

    file = request.files['file']

    # verify that the user has selected a file
    if file.filename == '':
        flash('No file was selected')
        return redirect(url_for('home'))

    # otherwise, try reading in the data
    try:
        data = read_data(request.files['file'])
        print(data.head())
    except FileNotFoundError as e:
        logging.warning(e)
        return {"success": False}

    # upload to data folder
    filename = secure_filename(file.filename)
    data.to_csv(app.config['UPLOAD_FOLDER'] + filename)

    return redirect(url_for('home'))


@app.route('/download')
def download():

    # check if the data folder is empty
    if not os.listdir(app.config['UPLOAD_FOLDER']):
        return redirect(url_for('home'))

    return redirect(url_for('download_file', file=os.listdir(app.config['UPLOAD_FOLDER'])[0]))


@app.route('/download/<file>', methods=['GET'])
def download_file(file):
    return send_file(app.config['UPLOAD_FOLDER'] + file, download_name='fake_forecast.csv')


if __name__ == '__main__':
    # app.secret_key = 'super secret key'
    app.run(host='0.0.0.0', port=5002)

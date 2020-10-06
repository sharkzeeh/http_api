from flask import Flask, request
import os, sys, hashlib
from pathlib import Path


app = Flask(__name__)
store_path = os.getcwd() + '/' + 'store'
downloads = str(Path.home()) + '/Downloads'


def reader(loc, mode):
    with open(loc, mode) as fh: 
        r = fh.read()
    return r


def writer(loc, mode, content):
    with open(loc, mode) as fh:
        fh.write(content)


def hasher(text):
    m = hashlib.md5()
    m.update(text)
    return m.hexdigest()


@app.route('/', methods=['GET'])
def hello():
    return '<h1>Welcome to the root page!</h1>'


@app.route('/upload', methods=['POST'])
def upload():
    dat = request.data
    hsh = hasher(request.data)
    folder = hsh[:2]
    temp_path = store_path + '/' + folder
    abs_path = temp_path + '/' + hsh
    if folder not in os.listdir(store_path):
        os.makedirs(temp_path)
        if hsh not in os.listdir(temp_path):
            writer(abs_path, 'wb', dat)
            return 'uploaded!'
        else:
            return 'the file has already been uploaded!'
    else:
        if hsh not in os.listdir(temp_path):
            writer(abs_path, 'wb', dat)
            return 'uploaded!'
        else:
            return 'the file has already been uploaded!'
    return 'uploaded!'


@app.route('/download/<hash>', methods=['GET'])
def download(file_hash):
    folder = file_hash[:2]
    if folder in os.listdir(store_path):
        temp_path = store_path + '/' + folder
        if file_hash in os.listdir(temp_path):
            file_loc = temp_path + '/' + file_hash
            down_loc = downloads + '/' + file_hash
            try:
                r = reader(file_loc, 'r')
                writer(down_loc, 'w', r)
            except UnicodeDecodeError:
                r = reader(file_loc, 'rb')
                writer(down_loc, 'wb', r)
            return 'downloaded!'
        else:
            return 'No such file'
    else:
        return 'No such file'


@app.route('/delete/<file_hash>', methods=['DELETE'])
def delete(file_hash):
    folder = file_hash[:2]
    if folder in os.listdir(store_path):
        temp_path = store_path + '/' + folder

        # if a 'ab' folder is empty
        if not os.listdir(temp_path):
            os.removedirs(store_path+'/'+folder)
            return 'No such file'

        if file_hash in os.listdir(temp_path):
            file_loc = temp_path + '/' + file_hash
            os.remove(file_loc)
            return 'removed!'
        else:
            return 'No such file'

    else:
        return 'No such file'
 

if __name__ == '__main__':
    app.run(debug=True)
    # export FLASK_APP=flask_app.py
    # export FLASK_DEBUG=1
    # curl -X POST -d  -H'Content-Type: image/jpg' localhost:5000/upload
    # curl -X POST --data-binary '@/home/robez/daemon/store/test.jpg' -H'Content-Type: application/octet-stream' localhost:5000/upload
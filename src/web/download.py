import os
import requests
import json
from flask import request, jsonify, Response
from tqdm import tqdm

DOWNLOAD_PATH = {}
APP = None;

def set_download_config(app, path):
    global APP, DOWNLOAD_PATH
    APP = app
    DOWNLOAD_PATH = path

def options():
    global APP
    with APP.app_context():
        return jsonify(DOWNLOAD_PATH)

def download(key):
    global APP, DOWNLOAD_PATH
    with APP.app_context():
        url = request.form['url']
        file_name = url.split('/')[-1]
        download_path = DOWNLOAD_PATH[key]
        file_path = os.path.join(download_path, file_name)

        def generate():
            response = requests.get(url, stream=True)
            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024
            progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)
            with open(file_path, 'wb') as f:
                for data in response.iter_content(block_size):
                    progress_bar.update(len(data))
                    f.write(data)
                    status = {'current': progress_bar.n, 'total': progress_bar.total}
                    yield json.dumps(status)
            progress_bar.close()

        return Response(generate(), mimetype='text/event-stream')
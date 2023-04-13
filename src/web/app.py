import os
from flask import Flask, render_template, request
from plot import plot_graph
from download import options, download, set_download_config
import json

app = Flask(__name__)

CONFIG_PATH = '../../config/config.json'
HOST = {'host': 'localhost', 'port': 7778}

def read_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r') as f:
            config = json.load(f)
        set_download_config(app, config['download'])
        global HOST
        HOST = config['server']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plot')
def plot():
    time = request.args.get('max_time', default=1)
    plot_graph(int(time))
    plot_file = os.path.join('static', 'plot.png')
    return render_template('plot.html', plot=plot_file)

@app.route('/download')
def download_page():
    return render_template('download.html')

@app.route('/action/options')
def action_options():
    return options()

@app.route('/action/download/<key>', methods=['POST'])
def action_download(key):
    return download(key)

if __name__ == '__main__':
    read_config()
    host = HOST['host']
    port = int(HOST['port'])
    app.run(host=host, port=port, debug=False)

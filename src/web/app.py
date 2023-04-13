import os
from flask import Flask, render_template, request
from plot import plot_graph
import json

app = Flask(__name__)
config_file = '../../config/config.json'
default_config = {'host': 'localhost', 'port': 7778}

if os.path.exists(config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)['server']
else:
    config = default_config

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/plot')
def plot():
    time = request.args.get('max_time', default=1)
    plot_graph(int(time))
    plot_file = os.path.join('static', 'plot.png')
    return render_template('plot.html', plot=plot_file)

if __name__ == '__main__':
    host = config['host']
    port = int(config['port'])
    app.run(host=host, port=port, debug=False)

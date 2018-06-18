from flask import render_template, Response, send_from_directory

from emulator import app


@app.route('/')
def index():
    app.logger.warning('sample message')
    return render_template('index.html')

@app.route('/getSituation')
def getSituation():
    app.logger.warning('Get situation')
    return send_from_directory('static', 'situation.json', mimetype='application/json')

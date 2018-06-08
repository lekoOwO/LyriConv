from flask import Flask, request
import lyric
import os

port = int(os.getenv('PORT', 8080))
host = int(os.getenv('HOST', '0.0.0.0'))

app = Flask(__name__)

@app.route('/migrate', methods=['POST'])
def migrate():
    return lyric.migrate(request.form['org'], request.form['cht'] if 'cht' in request.form else lyric.chs_to_cht(request.form['chs'])) 

app.run(host=port=port)
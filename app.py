from flask import Flask, request
import lyric
import os

port = int(os.getenv('PORT', 8080))
host = os.getenv('HOST', '0.0.0.0')

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024

@app.route('/migrate', methods=['POST'])
def migrate():
    org = request.form['org'] if 'org' in request.form else request.files['org'].read()
    translated_lang = 'cht' if 'cht' in (request.form or request.files) else 'chs'
    translated = request.form[translated_lang] if translated_lang in request.form else request.files[translated_lang].read()
    if translated_lang == 'chs':
        translated = lyric.chs_to_cht(translated) 
    return lyric.migrate(org, translated)

app.run(host=host, port=port)
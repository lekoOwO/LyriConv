from flask import Flask, request, jsonify
import lyric
import os
from modules import mojim, netease

port = int(os.getenv('PORT', 8080))
host = os.getenv('HOST', '0.0.0.0')

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024

@app.route('/migrate', methods=['POST'])
def migrate():
    org = request.form['org'] if 'org' in request.form else request.files['org'].read().decode() 
    translated_lang = 'cht' if 'cht' in (request.form or request.files) else 'chs'
    translated = request.form[translated_lang] if translated_lang in request.form else request.files[translated_lang].read().decode() 
    if translated_lang == 'chs':
        translated = lyric.chs_to_cht(translated) 
    return lyric.migrate(org, translated)

@app.route('/search', methods=['GET', 'POST'])
def search():
    keyword = request.args.get('keyword')
    return jsonify({
        "mojim": mojim.search(keyword),
        "netease": netease.search(keyword),
        "code": 200
    })

@app.route('/lyric', methods=['POST'])
def lyric_():
    p = request.form['p']
    if (p == 'mojim'):
        url = request.form['url']
        return mojim.get_lyric(url)
    elif (p == 'netease'):
        id_ =  request.form['id']
        return jsonify(netease.get_lyric(id_))

app.run(host=host, port=port)

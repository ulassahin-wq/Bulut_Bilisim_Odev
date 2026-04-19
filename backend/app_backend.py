# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import redis, json
# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import redis, json

app = Flask(__name__)
CORS(app)


db = redis.Redis(host='db', port=6379, decode_responses=True)

@app.route('/kaydet', methods=['POST'])
def kaydet():
    try:
        data = request.json
        data['tarih'] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        db.lpush('liste', json.dumps(data))
        return jsonify({"durum": "basarili"}), 200
    except Exception as e:
        return jsonify({"durum": "hata", "mesaj": str(e)}), 500

@app.route('/oku', methods=['GET'])
def oku():
    veriler = db.lrange('liste', 0, -1)
    return jsonify([json.loads(v) for v in veriler])

@app.route('/sil', methods=['POST'])
def sil():
    db.delete('liste')
    return jsonify({"durum": "temizlendi"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001) 
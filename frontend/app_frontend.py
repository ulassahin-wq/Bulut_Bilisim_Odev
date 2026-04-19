# -*- coding: utf-8 -*-
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <title>Hava Kalite Takip Sistemi</title>
        <style>
            body { font-family: sans-serif; background: #0f172a; color: white; display: flex; justify-content: center; padding-top: 50px; }
            .panel { background: #1e293b; padding: 20px; border-radius: 10px; width: 350px; text-align: center; }
            input { width: 90%; padding: 10px; margin-bottom: 10px; border-radius: 5px; border: none; }
            button { width: 45%; padding: 10px; cursor: pointer; border-radius: 5px; border: none; font-weight: bold; }
            .btn-g { background: #38bdf8; } .btn-s { background: #ef4444; color: white; }
            .item { background: #334155; padding: 10px; margin-top: 10px; border-radius: 5px; text-align: left; font-size: 14px; }
        </style>
    </head>
    <body>
        <div class="panel">
            <h2>HAVA KALİTE PANELİ</h2>
            <input type="text" id="sehir" placeholder="Şehir">
            <input type="number" id="deger" placeholder="AQI">
            <button onclick="kaydet()" class="btn-g">Gönder</button>
            <button onclick="temizle()" class="btn-s">Sil</button>
            <div id="liste"></div>
        </div>
        <script>
            // KRİTİK: Tarayıcıdan erişim için localhost kullanılmalı
            const API = 'http://localhost:5001';

            async function yenile() {
                const r = await fetch(`${API}/oku`);
                const data = await r.json();
                document.getElementById('liste').innerHTML = data.map(d => `
                    <div class="item"><b>${d.sehir}</b>: ${d.deger} AQI <br> <small>${d.tarih}</small></div>
                `).join('');
            }
            async function kaydet() {
                const s = document.getElementById('sehir').value;
                const v = document.getElementById('deger').value;
                await fetch(`${API}/kaydet`, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ sehir: s, deger: v })
                });
                yenile();
            }
            async function temizle() {
                await fetch(`${API}/sil`, { method: 'POST' });
                yenile();
            }
            yenile();
        </script>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
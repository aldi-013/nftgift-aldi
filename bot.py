from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Fungsi untuk koneksi database
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # Mengembalikan data dalam bentuk dictionary
    return conn

# Route untuk halaman utama
@app.route('/')
def index():
    conn = get_db_connection()
    data = conn.execute('SELECT * FROM nft_auction').fetchall()
    conn.close()
    return render_template('index.html', items=data)

# API untuk mendapatkan data JSON
@app.route('/api/data', methods=['GET'])
def get_data():
    conn = get_db_connection()
    data = conn.execute('SELECT * FROM nft_auction').fetchall()
    conn.close()
    return jsonify([dict(row) for row in data])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
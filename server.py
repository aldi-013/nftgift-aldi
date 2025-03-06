from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

def get_all_gifts():
    """ Mengambil semua data NFT dari database """
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT contact, name, model, background, symbol, series, price, link FROM gifts")
    data = cursor.fetchall()
    conn.close()

    # Format data ke JSON
    gifts = []
    for row in data:
        gifts.append({
            "contact": row[0],
            "name": row[1],
            "model": row[2],
            "background": row[3],
            "symbol": row[4],
            "series": row[5],
            "price": row[6],
            "link": row[7],
        })
    
    return gifts

@app.route("/api/gifts", methods=["GET"])
def api_get_gifts():
    return jsonify(get_all_gifts())
    
# Endpoint untuk mengambil semua NFT dari database
@app.route('/api/nfts', methods=['GET'])
def get_nfts():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, model, background, symbol, series, price, link FROM gifts")
    nfts = [{"name": row[0], "model": row[1], "background": row[2], "symbol": row[3], "series": row[4], "price": row[5], "link": row[6]} for row in cursor.fetchall()]
    conn.close()
    return jsonify(nfts)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

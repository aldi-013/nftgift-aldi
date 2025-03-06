import sqlite3
import re
import logging
from telethon import TelegramClient, events
from config import API_ID, API_HASH, BOT_TOKEN

# Konfigurasi logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# Inisialisasi bot
bot = TelegramClient("nftbot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# Buat database jika belum ada
conn = sqlite3.connect("database.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS gifts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    contact TEXT NOT NULL,
    name TEXT NOT NULL,
    model TEXT NOT NULL,
    background TEXT NOT NULL,
    symbol TEXT NOT NULL,
    series TEXT NOT NULL,
    price TEXT NOT NULL,
    link TEXT UNIQUE NOT NULL
)
""")
conn.commit()
conn.close()

def add_gift(contact, name, model, background, symbol, series, price, link):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO gifts (contact, name, model, background, symbol, series, price, link) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (contact, name, model, background, symbol, series, price, link))
        conn.commit()
        response = "✅ NFT berhasil disimpan!"
    except sqlite3.IntegrityError:
        response = "⚠️ NFT sudah ada dalam database."

    conn.close()
    return response

@bot.on(events.NewMessage(pattern=r"^/post$"))
async def post_nft(event):
    if event.is_reply:
        reply_msg = await event.get_reply_message()
        text = reply_msg.text.strip()

        # Perbaikan regex untuk menangkap format dengan benar
        match = re.search(r"contact : (.+)\nnama gift : (.+)\nmodel : (.+)\nlatar : (.+)\nsimbol : (.+)\nseri : #?(\d+)\nharga : (.+)\nlink : (https:\/\/t\.me\/[A-Za-z0-9\-_]+\/[A-Za-z0-9\-_]+)", text)

        if match:
            contact, name, model, background, symbol, series, price, link = match.groups()
            series = f"#{series}"  # Tambahkan "#" secara manual jika hilang
            response = add_gift(contact, name, model, background, symbol, series, price, link)
            await event.reply(response)
        else:
            await event.reply("⚠️ Format tidak sesuai! Pastikan format pesan sesuai.")
    else:
        await event.reply("⚠️ Gunakan perintah ini dengan mereply pesan yang berisi informasi NFT.")

# Jalankan bot
print("✅ Bot berjalan...")
bot.run_until_disconnected()
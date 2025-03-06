import sqlite3
import re
from telethon import TelegramClient, events
from config import API_ID, API_HASH, BOT_TOKEN

API_ID = 24576633  # Ganti dengan API ID Anda
API_HASH = "29931cf620fad738ee7f69442c98e2ee"
BOT_TOKEN = "7826609414:AAF-F5xvU9vwBQdaG2-c1c2C3u8Ylw13bzc"

# Inisialisasi bot
bot = TelegramClient("nftbot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# Buat database jika belum ada
conn = sqlite3.connect("database.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS gifts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    link TEXT UNIQUE NOT NULL
)
""")
conn.commit()
conn.close()


# Fungsi untuk menambahkan NFT ke database
def add_gift(link):
    if not re.match(r"^https:\/\/t\.me\/nft\/[A-Za-z0-9\-_]+$", link):
        return "Format link NFT tidak valid! Gunakan: https://t.me/nft/..."
    
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO gifts (link) VALUES (?)", (link,))
        conn.commit()
        response = "✅ NFT berhasil disimpan!"
    except sqlite3.IntegrityError:
        response = "⚠️ NFT sudah ada dalam database."

    conn.close()
    return response


# Handler untuk perintah /post {link_nft}
@bot.on(events.NewMessage(pattern=r"^/post (.+)$"))
async def post_nft(event):
    link = event.pattern_match.group(1).strip()
    response = add_gift(link)
    await event.reply(response)


# Jalankan bot
print("Bot berjalan...")
bot.run_until_disconnected()

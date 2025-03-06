import sqlite3
import re
import logging
from telethon import TelegramClient, events
from config import API_ID, API_HASH, BOT_TOKEN

# Konfigurasi logging untuk debugging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

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
    # Pola regex yang lebih fleksibel untuk menangani berbagai format link
    pattern = r"^https:\/\/t\.me\/(?:c\/\d+\/\d+|[A-Za-z0-9\-_]+\/\d+)$"
    if not re.match(pattern, link):
        return "⚠️ Format link NFT tidak valid! Gunakan: https://t.me/xxx/123"
    
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
@bot.on(events.NewMessage(pattern=r"^/post (.+)", incoming=True))
async def post_nft(event):
    logging.debug(f"Pesan diterima: {event.raw_text}")

    if event.is_private or event.is_group:
        link = event.pattern_match.group(1).strip()
        response = add_gift(link)
        await event.reply(response)
        logging.debug(f"Balasan terkirim: {response}")

# Jalankan bot
print("✅ Bot berjalan...")
bot.run_until_disconnected()
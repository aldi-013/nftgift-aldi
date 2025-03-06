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

def add_gift(link):
    # Gunakan regex yang benar untuk menangani format link NFT
    pattern = r"^https:\/\/t\.me\/[A-Za-z0-9\-_]+\/[A-Za-z0-9\-_]+$"
    if not re.match(pattern, link):
        return "⚠️ Format link NFT tidak valid! Gunakan format yang benar seperti: https://t.me/nft/LolPop-173409"
    
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

@bot.on(events.NewMessage(pattern=r"^/post (.+)"))
async def post_nft(event):
    logging.debug(f"Pesan diterima: {event.raw_text}")

    if event.is_private or event.is_group:
        link = event.pattern_match.group(1).strip()
        logging.debug(f"Link NFT yang diterima: {link}")
        
        response = add_gift(link)
        logging.debug(f"Respon yang dikirim: {response}")
        
        await event.reply(response)

# Jalankan bot
print("✅ Bot berjalan...")
bot.run_until_disconnected()
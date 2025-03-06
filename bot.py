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

# Buat tabel jika belum ada
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

# Cek apakah kolom contact sudah ada, jika belum tambahkan
try:
    cursor.execute("ALTER TABLE gifts ADD COLUMN contact TEXT NOT NULL DEFAULT ''")
    conn.commit()
except sqlite3.OperationalError:
    pass  # Jika kolom sudah ada, abaikan error

conn.close()

def add_gift(contact, name, model, background, symbol, series, price, link):
    """ Menambahkan NFT ke database """
    pattern = r"^https:\/\/t\.me\/[A-Za-z0-9\-_]+\/[A-Za-z0-9\-_]+$"
    if not re.match(pattern, link):
        return "⚠️ Format link NFT tidak valid! Gunakan format seperti: https://t.me/nft/LolPop-173409"
    
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
    """ Menyimpan NFT dari pesan reply """
    if event.is_reply:
        reply_msg = await event.get_reply_message()
        text = reply_msg.text.strip()

        # Parsing format pesan menggunakan regex
        match = re.search(
            r"contact : (.+)\n"
            r"nama gift : (.+)\n"
            r"model : (.+)\n"
            r"latar : (.+)\n"
            r"simbol : (.+)\n"
            r"seri : #?(\d+)\n"
            r"harga : (.+)\n"
            r"link : (https:\/\/t\.me\/[A-Za-z0-9\-_]+\/[A-Za-z0-9\-_]+)", text, re.DOTALL
        )
        
        if match:
            contact, name, model, background, symbol, series, price, link = match.groups()
            response = add_gift(contact.strip(), name.strip(), model.strip(), background.strip(), 
                                symbol.strip(), f"#{series.strip()}", price.strip(), link.strip())
            await event.reply(response)
        else:
            await event.reply("⚠️ Format tidak sesuai! Pastikan format pesan seperti ini:\n\n"
                              "contact : @username\n"
                              "nama gift : Lol Pop\n"
                              "model : einstein\n"
                              "latar : lavender\n"
                              "simbol : pizza slice\n"
                              "seri : #173409\n"
                              "harga : 100.000\n"
                              "link : https://t.me/nft/LolPop-173409")
    else:
        await event.reply("⚠️ Gunakan perintah ini dengan mereply pesan yang berisi informasi NFT.")

# Jalankan bot
print("✅ Bot berjalan...")
bot.run_until_disconnected()
import requests
from bs4 import BeautifulSoup
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

KEYWORDS = ["Community", "Manager", "Social", "Marketing", "Content", "Growth", "BD", "Moderator", "Admin", "Support"]

def send_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
        requests.post(url, json=payload, timeout=10)
        print("✅ Pesan terkirim")
    except Exception as e:
        print(f"❌ Telegram error: {e}")

print("🔍 Mulai menjalankan scraper...")

url = "https://web3.career/"
headers = {"User-Agent": "Mozilla/5.0"}

r = requests.get(url, headers=headers)
print(f"Status Code: {r.status_code}")

soup = BeautifulSoup(r.text, 'html.parser')
rows = soup.select('tbody tr')

print(f"Ditemukan {len(rows)} lowongan")

sent = 0
for row in rows[:30]:
    try:
        title_tag = row.find('a')
        if not title_tag: continue
        title = title_tag.get_text(strip=True)
        link = "https://web3.career" + title_tag['href']
        
        if any(kw.lower() in title.lower() for kw in KEYWORDS):
            company = row.find_all('td')[1].get_text(strip=True) if len(row.find_all('td')) > 1 else ""
            msg = f"🔔 <b>Lowongan Web3!</b>\n\n📌 {title}\n🏢 {company}\n🔗 {link}"
            send_telegram(msg)
            print(f"✅ Match: {title[:60]}")
            sent += 1
    except:
        continue

print(f"Selesai. Total dikirim: {sent}")
if sent == 0:
    send_telegram("✅ Bot berjalan normal.\nTidak ada lowongan match hari ini.")

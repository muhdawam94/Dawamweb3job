import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

KEYWORDS = ["Community", "Manager", "Social", "Marketing", "Content", "Growth", 
            "BD", "Business Development", "Moderator", "Admin", "Support"]

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        requests.post(url, json=payload, timeout=10)
        print("✅ Telegram sent")
    except Exception as e:
        print(f"Telegram error: {e}")

def scrape_web3():
    print("🔍 Mulai scraping...")
    url = "https://web3.career/"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    r = requests.get(url, headers=headers, timeout=15)
    print(f"Status: {r.status_code}")
    
    soup = BeautifulSoup(r.text, 'html.parser')
    rows = soup.select('tbody tr')
    print(f"Ditemukan {len(rows)} lowongan")

    sent = 0
    for row in rows[:30]:
        try:
            a = row.find('a')
            if not a: continue
            title = a.get_text(strip=True)
            link = "https://web3.career" + a['href']
            
            if any(kw.lower() in title.lower() for kw in KEYWORDS):
                company = row.find_all('td')[1].get_text(strip=True) if len(row.find_all('td')) > 1 else ""
                msg = f"🔔 Lowongan Baru!\n\n{title}\n{company}\n{link}"
                send_telegram(msg)
                sent += 1
                print(f"✅ Match: {title[:60]}")
        except:
            continue
            
    print(f"Selesai. Dikirim {sent} lowongan")
    if sent == 0:
        send_telegram("✅ Bot jalan normal.\nTidak ada lowongan match hari ini.")

if __name__ == "__main__":
    scrape_web3()

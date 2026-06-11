import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

KEYWORDS = ["Community", "Manager", "Social Media", "Marketing", "Content", 
            "Executive", "Growth", "BD", "Business Development", "Partnership",
            "Moderator", "Admin", "Support", "Assistant", "Coordinator", "Social"]

checked_jobs = set()

def send_telegram(message):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("❌ TOKEN atau CHAT_ID kosong")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        requests.post(url, json=payload, timeout=10)
        print("✅ Pesan berhasil dikirim ke Telegram")
    except Exception as e:
        print(f"❌ Gagal kirim ke Telegram: {e}")

def scrape_web3():
    url = "https://web3.career/"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        print("🔍 Mulai scraping web3.career...")
        r = requests.get(url, headers=headers, timeout=15)
        print(f"📡 Status Code: {r.status_code}")
        
        soup = BeautifulSoup(r.text, 'html.parser')
        rows = soup.select('tbody tr')
        print(f"📊 Ditemukan {len(rows)} lowongan di halaman")
        
        new_jobs = 0
        for row in rows[:30]:
            try:
                link_tag = row.find('a', href=True)
                if not link_tag: 
                    continue
                    
                title = link_tag.get_text(strip=True)
                link = "https://web3.career" + link_tag['href']
                job_id = link.split('/')[-1]
                
                if job_id in checked_jobs:
                    continue
                
                tds = row.find_all('td')
                company = tds[1].get_text(strip=True) if len(tds) > 1 else "Unknown"
                
                match = any(kw.lower() in title.lower() for kw in KEYWORDS)
                print(f"Job: {title[:50]}... | Match: {match}")
                
                if match:
                    message = f"""
🔔 <b>Lowongan Web3 Baru!</b>

📌 <b>{title}</b>
🏢 {company}
🔗 {link}
                    """
                    send_telegram(message.strip())
                    checked_jobs.add(job_id)
                    new_jobs += 1
                    
            except:
                continue
                
        print(f"✅ Selesai. Total lowongan match: {new_jobs}")
        if new_jobs == 0:
            send_telegram("✅ Bot berjalan.\nTidak ada lowongan yang match keyword hari ini.")
            
    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        print(error_msg)
        send_telegram(error_msg)

if __name__ == "__main__":
    scrape_web3()

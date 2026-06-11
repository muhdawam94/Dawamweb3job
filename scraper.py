import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

# ================= CONFIG =================
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

KEYWORDS = ["Community", "Manager", "Social Media", "Marketing", "Content", 
            "Executive", "Growth", "BD", "Business Development", "Partnership"]

checked_jobs = set()

def send_telegram(message):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("❌ TELEGRAM_TOKEN atau CHAT_ID belum di-set")
        return
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        requests.post(url, json=payload, timeout=10)
    except:
        pass

def scrape_web3():
    url = "https://web3.career/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')
        
        rows = soup.select('tbody tr')[:30]
        
        new_jobs = 0
        for row in rows:
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
                posted = tds[2].get_text(strip=True) if len(tds) > 2 else ""
                
                if any(kw.lower() in title.lower() for kw in KEYWORDS):
                    message = f"""
🔔 <b>Lowongan Web3 Baru!</b>

📌 <b>{title}</b>
🏢 {company}
⏰ {posted}
🔗 {link}

🕒 {datetime.now().strftime('%d %B %Y, %H:%M WIB')}
                    """
                    send_telegram(message.strip())
                    checked_jobs.add(job_id)
                    new_jobs += 1
                    
            except:
                continue
                
        print(f"✅ Selesai. Ditemukan {new_jobs} lowongan baru.")
        
    except Exception as e:
        error_msg = f"❌ Error scraping: {str(e)}"
        print(error_msg)
        send_telegram(error_msg)

if __name__ == "__main__":
    scrape_web3()

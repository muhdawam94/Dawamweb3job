import requests
from bs4 import BeautifulSoup
from datetime import datetime

# ================= CONFIG =================
TELEGRAM_TOKEN = "8906551230:AAGpqr3w806c5YkmyGZN02uq-_pMZdrx61E"
CHAT_ID = "805652229"
KEYWORDS = ["Community", "Manager", "Social Media", "Marketing", "Content", "Executive"]

checked_jobs = set()

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        requests.post(url, json=payload)
    except:
        pass

def scrape_web3():
    url = "https://web3.career/"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        r = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        rows = soup.select('tbody tr')[:25]
        
        for row in rows:
            try:
                link_tag = row.find('a')
                if not link_tag or not link_tag.get('href'):
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
🔔 <b>Lowongan Baru!</b>

📌 <b>{title}</b>
🏢 {company}
⏰ {posted}
🔗 {link}

🕒 {datetime.now().strftime('%d %B %Y, %H:%M')}
                    """
                    send_telegram(message.strip())
                    checked_jobs.add(job_id)
            except:
                continue
    except Exception as e:
        send_telegram(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    scrape_web3()

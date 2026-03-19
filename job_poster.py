import requests
from bs4 import BeautifulSoup
import json
import os
import time

# Configuration
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')
HISTORY_FILE = 'job_history.json'
TARGET_URL = "https://ai-jobs.net"

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, 'r') as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except Exception as e:
        print(f"⚠️ History file error (Resetting): {e}")
        return []

def save_history(history):
    try:
        with open(HISTORY_FILE, 'w') as f:
            json.dump(history[-100:], f)
    except Exception as e:
        print(f"❌ Could not save history: {e}")

def send_telegram(message):
    if not TELEGRAM_TOKEN or not CHANNEL_ID:
        print("❌ Error: Missing Telegram Credentials.")
        return

    url = f"https://api.telegram.org{TELEGRAM_TOKEN}/sendMessage" 
    payload = {
        "chat_id": CHANNEL_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        print("✅ Message sent successfully!")
    except Exception as e:
        print(f"❌ Telegram API Error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Details: {e.response.text}")

def scrape_ai_jobs():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    job_list = []
    try:
        print(f"🔍 Fetching {TARGET_URL}...")
        response = requests.get(TARGET_URL, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        rows = soup.select('li.list-group-item')
        print(f"📊 Found {len(rows)} potential job rows.")

        for row in rows:
            try:
                title_element = row.select_one('h3 a')
                if not title_element: continue

                title = title_element.text.strip()
                href = title_element.get('href', '')
                link = href if href.startswith('http') else f"https://ai-jobs.net{href}"
                
                company_el = row.select_one('span.text-muted')
                company = company_el.text.strip() if company_el else "AI Company"
                
                tags =
                tag_str = " | ".join(tags) if tags else "Remote / Full-time"

                job_list.append({
                    "id": link,
                    "title": title,
                    "company": company,
                    "link": link,
                    "tags": tag_str
                })
            except Exception:
                continue # Skip individual job errors
        return job_list
    except Exception as e:
        print(f"❌ Scraping Failed: {e}")
        return []

def main():
    history = load_history()
    jobs = scrape_ai_jobs()
    
    if not jobs:
        print("⚠️ No jobs retrieved. Check the URL or Selectors.")
        return

    new_count = 0
    # Check top 10 newest jobs
    for job in reversed(jobs[:10]): 
        if job['id'] not in history:
            print(f"🆕 New Job: {job['title']}")
            
            post_text = (
                f"🤖 <b>NEW AI JOB POSTING</b>\n\n"
                f"🔥 <b>{job['title']}</b>\n"
                f"🏢 <i>{job['company']}</i>\n\n"
                f"📍 {job['tags']}\n"
                f"✅ Verified Role\n\n"
                f"🔗 <a href='{job['link']}'><b>VIEW AND APPLY</b></a>\n\n"
                f"#AI #AITraining #Jobs #AIGigHub"
            )
            
            send_telegram(post_text)
            history.append(job['id'])
            new_count += 1
            time.sleep(2) 
            
    if new_count > 0:
        save_history(history)
        print(f"✨ Done! Posted {new_count} new jobs.")
    else:
        print("😴 Everything is up to date.")

if __name__ == "__main__":
    main()

import requests
from bs4 import BeautifulSoup
import json
import os
import time

# 1. Configuration (Uses GitHub Secrets/Environment Variables)
TELEGRAM_TOKEN = os.getenv('8617577163:AAGh_UsAQccArBMhewYMTHhbbWD9N4xkrmE')
CHANNEL_ID = os.getenv('@AIGigHub')
HISTORY_FILE = 'job_history.json'
TARGET_URL = "https://ai-jobs.net"

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_history(history):
    # Keep only the last 100 job IDs to keep the file small
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history[-100:], f)

def send_telegram(message):
    url = f"https://api.telegram.org{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
    except Exception as e:
        print(f"Error sending to Telegram: {e}")

def scrape_ai_jobs():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        response = requests.get(TARGET_URL, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        job_list = []

        # Find job entries on ai-jobs.net
        for row in soup.select('li.list-group-item'):
            title_element = row.select_one('h3 a')
            if not title_element:
                continue

            title = title_element.text.strip()
            link = "https://ai-jobs.net" + title_element['href']
            
            # Get Company and Metadata
            company_element = row.select_one('span.text-muted')
            company = company_element.text.strip() if company_element else "AI Company"
            
            # Extract badges (Salary, Remote status, etc)
            tags = [tag.text.strip() for tag in row.select('.badge')]
            tag_str = " | ".join(tags) if tags else "Full-time"

            job_list.append({
                "id": link,
                "title": title,
                "company": company,
                "link": link,
                "tags": tag_str
            })
        return job_list
    except Exception as e:
        print(f"Scraping error: {e}")
        return []

def main():
    if not TELEGRAM_TOKEN or not CHANNEL_ID:
        print("Error: Missing TELEGRAM_TOKEN or CHANNEL_ID in Environment Variables.")
        return

    history = load_history()
    jobs = scrape_ai_jobs()
    
    # Process only the top 10 most recent jobs to avoid flooding
    new_jobs_found = 0
    for job in reversed(jobs[:10]): 
        if job['id'] not in history:
            # The HTML Format for Telegram
            post_text = (
                f"🤖 <b>NEW AI JOB POSTING</b>\n\n"
                f"🔥 <b>{job['title']}</b>\n"
                f"🏢 <i>{job['company']}</i>\n\n"
                f"📍 {job['tags']}\n"
                f"✅ Verified AI Training Role\n\n"
                f"🔗 <a href='{job['link']}'><b>VIEW AND APPLY</b></a>\n\n"
                f"#AI #AITraining #Jobs #Remote #AIGigHub"
            )
            
            send_telegram(post_text)
            print(f"Posted: {job['title']}")
            
            history.append(job['id'])
            new_jobs_found += 1
            time.sleep(3) # Small delay between posts
            
    if new_jobs_found > 0:
        save_history(history)
    else:
        print("No new jobs found this cycle.")

if __name__ == "__main__":
    main()

# 🤖 AI Training Jobs - Telegram Automator

This repository hosts a Python-based automation tool that tracks the latest AI Training, RLHF, and Data Annotation jobs from top job boards and automatically broadcasts them to the [AI Training Jobs Telegram Channel](https://t.me).

## 🚀 How It Works
- **Scraper:** Built with `Python` and `BeautifulSoup` to parse job listings.
- **Automation:** Powered by `GitHub Actions`, running on a schedule (every 6 hours).
- **History Tracking:** Uses `job_history.json` to ensure no duplicate jobs are ever posted.
- **Formatting:** Jobs are automatically converted into Telegram-compatible HTML with specialized tags.

## 🛠️ Tech Stack
- **Language:** Python 3.10+
- **Libraries:** Requests, BeautifulSoup4
- **Deployment:** GitHub Actions (Serverless)

## 📁 Project Structure
- `job_poster.py`: The core logic for scraping and posting.
- `job_history.json`: Local database to track already posted jobs.
- `.github/workflows/scrape.yml`: The automation schedule.
- `requirements.txt`: Python dependencies.

## ⚙️ Setup & Deployment
If you want to fork this and run your own version:

1. **Clone the repo:**
   ```bash
   git clone https://github.com
   cd ai-job-bot

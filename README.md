# 🤖 AI Training Jobs - Telegram Automator (v1.0)

An automated pipeline designed to bridge the gap between AI Talent and high-value opportunities. This bot monitors specialized job boards and broadcasts formatted listings to the [AI Training Jobs Telegram Channel](https://t.me).

## 🎯 Project Overview
This project automates the sourcing and distribution of "Human-in-the-Loop" (HITL) and AI Training roles. It eliminates the manual work of checking job boards by using a scheduled scraper that identifies, cleans, and posts new opportunities every 6 hours.

## 📡 Data Sources (v1.0)
Currently, the bot fetches and processes live data from:
*   **[AI-Jobs.net](https://ai-jobs.net)**: A primary hub for Machine Learning, Data Science, and AI Training roles.
*   *Upcoming in v1.1:* Integration for Outlier.ai, DataAnnotation.tech, and Greenhouse/Lever API filtering.

## 🚀 Key Features
- **Smart Scraper:** Utilizes `BeautifulSoup4` with custom headers to parse HTML structures from modern job boards.
- **Serverless Automation:** Managed entirely via `GitHub Actions`, requiring zero hosting costs.
- **Deduplication Engine:** A local `job_history.json` database prevents the bot from posting the same job twice.
- **Rich Formatting:** Posts are delivered in Telegram-native HTML with bold headers, italicized company names, and easy-to-tap "Apply" links.

## 🛠️ Tech Stack
- **Language:** Python 3.10+
- **Network:** `Requests` (HTTP handling)
- **Parser:** `BeautifulSoup4` (HTML/CSS Selectors)
- **CI/CD:** GitHub Actions (Automated scheduling)

## 📁 Repository Structure
- `job_poster.py`: Core logic for fetching, filtering, and broadcasting.
- `.github/workflows/scrape.yml`: The YAML configuration for the 6-hour cron job.
- `job_history.json`: Persistence layer for tracking processed IDs.
- `requirements.txt`: Environment dependencies.

## ⚙️ Deployment Instructions

1. **Secrets Configuration:**
   Add these to your GitHub Repository (**Settings > Secrets > Actions**):
   - `TELEGRAM_TOKEN`: Your API token from [@BotFather](https://t.me).
   - `CHANNEL_ID`: Your channel handle (e.g., `@AIGigHub`).

2. **GitHub Actions Permissions:**
   Ensure your Workflow has "Read and Write" permissions under **Settings > Actions > General** so the bot can save the job history back to the repo.

3. **Manual Trigger:**
   Go to the **Actions** tab → **AI Job Scraper** → **Run workflow** to force a scrape immediately.

---
*Developed for the AI Community. Version 1.0 Stable.*

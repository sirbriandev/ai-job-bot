name: AI Job Scraper Automation

on:
  schedule:
    - cron: '0 */6 * * *'
  workflow_dispatch:

env:
  FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true

jobs:
  run-scraper:
    runs-on: ubuntu-latest
    permissions:
      contents: write # Essential for the bot to save history
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run the Bot
        env:
          TELEGRAM_TOKEN: ${{ secrets.TELEGRAM_TOKEN }}
          CHANNEL_ID: ${{ secrets.CHANNEL_ID }}
        run: python job_poster.py

      - name: Auto-commit and Push Changes
        uses: stefanzweifel/git-auto-commit-action@v5
        with:
          commit_message: "Update job history [skip ci]"
          file_pattern: 'job_history.json'

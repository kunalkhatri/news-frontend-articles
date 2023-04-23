#!/bin/bash
source venv/bin/activate
python step1.py

current_date_time=$(date)
git add .
git commit -m "new update for date $current_date_time"
git push

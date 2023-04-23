source venv/bin/activate
python step1.py
cd articles

current_date_time=$(date)

git add .

git commit -m "new update for date $current_date_time"

git push
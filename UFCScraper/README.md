& "C:\Users\danhm\AppData\Local\pypoetry\Cache\virtualenvs\ufcscraper-QpJUrYet-py3.9\Scripts\activate.ps1"
cd .\UFCScraper\
scrapy crawl ufc_scraper -o competitions.csv
scrapy crawl ufc_fighter_scraper -o individuals.csv
python fix_csvs.py
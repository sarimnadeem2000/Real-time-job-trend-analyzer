import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time

def scrape_indeed(keyword="Software Engineer", location="Pakistan", limit=50):
    headers = {"User-Agent": "Mozilla/5.0"}
    jobs = []
    base_url = f"https://pk.indeed.com/jobs?q={keyword}&l={location}"
    
    for start in range(0, limit, 10):
        url = f"{base_url}&start={start}"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        cards = soup.select('div.job_seen_beacon')
        
        for card in cards:
            title = card.find('h2').text.strip() if card.find('h2') else 'N/A'
            company = card.find('span', class_='companyName')
            location = card.find('div', class_='companyLocation')
            posted = card.find('span', class_='date')
            
            jobs.append({
                "title": title,
                "company": company.text.strip() if company else 'N/A',
                "location": location.text.strip() if location else 'N/A',
                "skills": "N/A",  # Indeed doesn't list detailed skills
                "date_posted": posted.text.strip() if posted else datetime.now().strftime("%Y-%m-%d")
            })
        time.sleep(1)  # polite delay
    return jobs

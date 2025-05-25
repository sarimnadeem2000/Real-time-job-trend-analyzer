import sqlite3

import pandas as pd

def init_db():
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT, company TEXT, location TEXT, skills TEXT, date_posted TEXT
    )''')
    conn.commit()
    conn.close()

def insert_jobs(jobs):
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    for job in jobs:
        c.execute("INSERT INTO jobs (title, company, location, skills, date_posted) VALUES (?, ?, ?, ?, ?)",
                  (job['title'], job['company'], job['location'], job['skills'], job['date_posted']))
    conn.commit()
    conn.close()

def fetch_all_jobs():
    conn = sqlite3.connect('jobs.db')
    df = pd.read_sql_query("SELECT * FROM jobs", conn)
    conn.close()
    return df

import pandas as pd
from collections import Counter

def get_top_titles(df):
    return df['title'].value_counts().head(5)

def get_top_locations(df):
    return df['location'].value_counts().head(5)

def get_top_skills(df):
    skills_series = df['skills'].dropna().str.split(',')
    flat_skills = [skill.strip() for sublist in skills_series for skill in sublist if skill]
    return Counter(flat_skills).most_common(5)

def get_posting_trend(df):
    df['date_posted'] = pd.to_datetime(df['date_posted'], errors='coerce')
    return df.groupby(df['date_posted'].dt.date).size()

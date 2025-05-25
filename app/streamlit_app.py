import pandas as pd
import streamlit as st
from app.scraper.indeed_scraper import scrape_indeed
from app.scraper.rozee_scraper import scrape_rozee
from app.database.db_handler import init_db, insert_jobs, fetch_all_jobs
from app.analyzer.analytics import get_top_titles, get_top_locations, get_top_skills, get_posting_trend
import plotly.express as px

init_db()

st.title("🔍 Real-Time Job Trend Analyzer")

if st.button("🔄 Fetch Latest Jobs"):
    jobs_indeed = scrape_indeed()
    insert_jobs(jobs_indeed)
    st.success(f"{len(jobs_indeed)} jobs fetched from Indeed.")

df = fetch_all_jobs()

if df.empty:
    st.warning("No job data available. Please fetch jobs first.")
else:
    st.subheader("Top 5 Job Titles")
    st.bar_chart(get_top_titles(df))

    st.subheader("Top Hiring Cities")
    st.bar_chart(get_top_locations(df))

    st.subheader("Most In-Demand Skills")
    skills = get_top_skills(df)
    st.write(pd.DataFrame(skills, columns=["Skill", "Count"]))

    st.subheader("Posting Trends Over Time")
    trends = get_posting_trend(df)
    fig = px.line(x=trends.index, y=trends.values, labels={"x": "Date", "y": "Number of Postings"})
    st.plotly_chart(fig)

    st.subheader("🔍 Filter by Keyword")
    keyword = st.text_input("Enter job keyword (e.g., Data Analyst)")
    if keyword:
        filtered = df[df['title'].str.contains(keyword, case=False)]
        st.write(filtered[['title', 'company', 'location', 'date_posted']])

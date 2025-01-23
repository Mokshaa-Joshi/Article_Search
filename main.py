import streamlit as st
import requests
from bs4 import BeautifulSoup

# Define function to scrape articles based on newspaper selection
def scrape_articles(newspaper, keyword):
    articles = []
    
    if newspaper == "Sandesh":
        url = f"https://www.sandesh.com/search?search={keyword}"
    elif newspaper == "Divya Bhaskar":
        url = f"https://www.divyabhaskar.co.in/search/?search={keyword}"
    elif newspaper == "Gujarat Samachar":
        url = f"https://www.gujaratsamachar.com/search?q={keyword}"
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Modify this part based on the newspaper's HTML structure
    for item in soup.find_all('article'):  # Adjust based on actual HTML structure
        headline = item.find('h2').get_text() if item.find('h2') else "No headline"
        content = item.find('p').get_text() if item.find('p') else "No content"
        link = item.find('a')['href'] if item.find('a') else "#"
        date = item.find('time').get_text() if item.find('time') else "No date"
        
        articles.append({
            'headline': headline,
            'content': content,
            'link': link,
            'date': date
        })
    
    return articles

# Streamlit UI Layout
st.title("Gujarati Newspaper Article Search")
st.sidebar.title("Select Newspaper")
newspaper = st.sidebar.selectbox("Choose a Newspaper", ["Sandesh", "Divya Bhaskar", "Gujarat Samachar"])
keyword = st.text_input("Enter Keyword")

if keyword:
    st.sidebar.text("Searching for articles...")
    articles = scrape_articles(newspaper, keyword)
    
    if articles:
        for article in articles:
            st.subheader(f"Headline: {article['headline']}")
            st.write(f"Content: {article['content']}")
            st.write(f"Date: {article['date']}")
            st.write(f"Link: [Read more]({article['link']})")
    else:
       

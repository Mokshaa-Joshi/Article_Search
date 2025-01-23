import streamlit as st
import requests
from bs4 import BeautifulSoup

# Function to fetch articles based on newspaper selection and search term
def fetch_articles(newspaper, keyword):
    # You will need to define the specific URLs and scraping logic for each newspaper.
    if newspaper == "Sandesh":
        url = "https://www.sandesh.com"  # Example, replace with actual URL
    elif newspaper == "Divya Bhaskar":
        url = "https://www.divyabhaskar.co.in"  # Example, replace with actual URL
    elif newspaper == "Gujarat Samachar":
        url = "https://www.gujaratsamachar.com"  # Example, replace with actual URL
    
    # Perform a request to fetch the page content
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Example scraping logic (adjust selectors for each site)
    articles = []
    for article in soup.find_all('article'):  # Adjust tag and class as needed
        headline = article.find('h2').text
        content = article.find('p').text
        link = article.find('a')['href']
        date = article.find('time').text
        
        # Check if the keyword matches the article content
        if keyword.lower() in headline.lower() or keyword.lower() in content.lower():
            articles.append({
                'headline': headline,
                'content': content,
                'link': link,
                'date': date
            })
    
    return articles

# Streamlit interface
st.title("Gujarati News Search")

# Dropdown for selecting newspaper
newspaper = st.sidebar.selectbox(
    "Select Newspaper",
    ["Sandesh", "Divya Bhaskar", "Gujarat Samachar"]
)

# Search bar for entering the keyword
keyword = st.text_input("Enter keyword")

# Display articles if keyword is entered
if keyword:
    articles = fetch_articles(newspaper, keyword)
    
    if articles:
        for article in articles:
            st.subheader(article['headline'])
            st.write(f"Date: {article['date']}")
            st.write(f"[Read more]({article['link']})")
            st.write(article['content'])
    else:
        st.write("No articles found for the given keyword.")

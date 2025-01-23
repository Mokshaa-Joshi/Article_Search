import streamlit as st
import requests
from bs4 import BeautifulSoup

# Function to fetch articles based on newspaper selection and search term
def fetch_articles(newspaper, keyword):
    # Define URLs for each newspaper (replace these with correct ones)
    if newspaper == "Sandesh":
        url = "https://www.sandesh.com"  # Replace with actual URL
    elif newspaper == "Divya Bhaskar":
        url = "https://www.divyabhaskar.co.in"  # Replace with actual URL
    elif newspaper == "Gujarat Samachar":
        url = "https://www.gujaratsamachar.com"  # Replace with actual URL
    
    # Send HTTP request
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if request was successful
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data from {newspaper}: {e}")
        return []

    # Parse HTML content with BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Example scraping logic, adjust based on actual page structure
    articles = []
    print(f"Scraping articles from {newspaper}...")
    for article in soup.find_all('article'):  # Adjust the tag for each newspaper
        headline = article.find('h2')
        if headline:
            headline = headline.text.strip()
        else:
            continue

        content = article.find('p')
        if content:
            content = content.text.strip()
        else:
            content = "No content available."

        link = article.find('a')['href'] if article.find('a') else "No link available"
        date = article.find('time')
        date = date.text.strip() if date else "No date available"
        
        # Debugging print statements
        print(f"Found article: {headline}")
        print(f"Link: {link}")
        print(f"Date: {date}")
        
        # Check if keyword is present in headline or content (case-insensitive)
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

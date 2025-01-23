import streamlit as st
from bs4 import BeautifulSoup
import requests
from datetime import datetime

# Define newspaper URLs and their Gujarati names
newspapers = {
    "સંદેશ": "https://www.sandesh.com/",
    "દિવ્ય ભાસ્કર": "https://www.divyabhaskar.co.in/",
    "ગુજરાત સમાચાર": "https://www.gujaratsamachar.com/"
}

def get_articles(newspaper_url, keyword):
    try:
        response = requests.get(newspaper_url)
        response.raise_for_status()  # Raise an exception for bad status codes
        soup = BeautifulSoup(response.content, "html.parser")

        # **Important:** This part needs to be adjusted based on the actual HTML 
        # structure of the specific newspaper websites. 
        # Example (This is a placeholder, adjust accordingly):
        articles = soup.find_all("div", class_="article-item") 

        results = []
        for article in articles:
            try:
                headline = article.find("h2").text.strip()
                # Extract a portion of the content (adjust as needed)
                content = article.find("p").text.strip()[:200] + "..." 
                link = article.find("a", href=True)["href"]

                # Example date extraction (adjust based on website structure)
                date_str = article.find("span", class_="date").text.strip() 
                date = datetime.strptime(date_str, "%d-%m-%Y") 

                results.append({
                    "headline": headline,
                    "content": content,
                    "link": link,
                    "date": date.strftime("%d-%m-%Y") 
                })
            except AttributeError:
                continue  # Skip articles with missing elements

        return results
    except requests.exceptions.RequestException as e:
        st.error(f"દત્તા મેળવવામાં ભૂલ: {newspaper_url} થી: {e}")
        return []

# Streamlit app
st.title("ગુજરાતી અખબાર શોધ")

selected_newspaper = st.selectbox("અખબાર પસંદ કરો", list(newspapers.keys()))
keyword = st.text_input("કીવર્ડ દાખલ કરો")

if st.button("શોધ"):
    articles = get_articles(newspapers[selected_newspaper], keyword)

    if articles:
        st.success(f"{selected_newspaper} માં {len(articles)} લેખો મળ્યા")
        for article in articles:
            st.subheader(article["headline"])
            st.write(article["content"])
            st.write(f"લિંક: {article['link']}")
            st.write(f"તારીખ: {article['date']}")
    else:
        st.info("કોઈ લેખ મળ્યો નથી.")

import streamlit as st
import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator

# Function to scrape Sandesh
def scrape_sandesh(keyword):
    url = f"https://www.sandesh.com/searchresults?searchkey={keyword}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    articles = []
    for item in soup.find_all("div", class_="listing-item"):
        try:
            headline = item.find("h2").text.strip()
            link = "https://www.sandesh.com" + item.find("a")["href"]
            content = item.find("p").text.strip()
            date = item.find("span", class_="post-time").text.strip()
            articles.append({"headline": headline, "content": content, "link": link, "date": date})
        except AttributeError:
            continue
    return articles

# Function to scrape Divya Bhaskar
def scrape_divyabhaskar(keyword):
    url = f"https://www.divyabhaskar.com/search/{keyword}/all"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    articles = []
    for item in soup.find_all("div", class_="Cardstyles__Container-sc-1d6xkg6-0"):
        try:
            headline = item.find("h3").text.strip()
            link = "https://www.divyabhaskar.com" + item.find("a")["href"]
            content = item.find("p").text.strip() if item.find("p") else "No content available."
            date = item.find("span", class_="time").text.strip() if item.find("span", class_="time") else "No date available."
            articles.append({"headline": headline, "content": content, "link": link, "date": date})
        except AttributeError:
            continue
    return articles

# Function to scrape Gujarat Samachar
def scrape_gujaratsamachar(keyword):
    url = f"https://www.gujaratsamachar.com/searchresult/{keyword}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    articles = []
    for item in soup.find_all("div", class_="content-row"):
        try:
            headline = item.find("h3").text.strip()
            link = item.find("a")["href"]
            content = item.find("p").text.strip() if item.find("p") else "No content available."
            date = item.find("span", class_="date").text.strip() if item.find("span", class_="date") else "No date available."
            articles.append({"headline": headline, "content": content, "link": link, "date": date})
        except AttributeError:
            continue
    return articles

# Main function
def main():
    st.title("Gujarati News Search")
    st.sidebar.header("Search Options")

    # Dropdown for newspaper selection
    newspaper = st.sidebar.selectbox(
        "Select Newspaper",
        ["Sandesh", "Divya Bhaskar", "Gujarat Samachar"]
    )

    # Search bar for keyword input
    keyword = st.sidebar.text_input("Enter a keyword to search (in any language):", "")

    # Search button
    if st.sidebar.button("Search"):
        if not keyword:
            st.warning("Please enter a keyword to search.")
            return

        # Translate keyword to Gujarati
        translator = GoogleTranslator(source="auto", target="gu")
        translated_keyword = translator.translate(keyword)
        st.write(f"Searching for articles with keyword: **{translated_keyword}** ({keyword})")

        # Scraping logic based on selected newspaper
        if newspaper == "Sandesh":
            articles = scrape_sandesh(translated_keyword)
        elif newspaper == "Divya Bhaskar":
            articles = scrape_divyabhaskar(translated_keyword)
        elif newspaper == "Gujarat Samachar":
            articles = scrape_gujaratsamachar(translated_keyword)
        else:
            articles = []

        # Display results
        if articles:
            st.success(f"Found {len(articles)} articles!")
            for article in articles:
                st.subheader(article["headline"])
                st.write(article["content"])
                st.write(f"**Published on:** {article['date']}")
                st.markdown(f"[Read more]({article['link']})")
                st.write("---")
        else:
            st.warning("No articles found. Try a different keyword.")

if __name__ == "__main__":
    main()

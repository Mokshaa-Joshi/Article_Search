import streamlit as st
import requests
from bs4 import BeautifulSoup


# Generalized scraping function
def scrape_general(url, keyword):
    """
    Scrapes articles and links from a given URL using a keyword.
    - url: The base URL of the website or search page.
    - keyword: The search keyword.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad HTTP responses
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching URL {url}: {e}")
        return []

    # Parse the HTML content
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all text-based elements and links
    articles = []
    for tag in soup.find_all(["p", "h1", "h2", "h3", "a"]):  # Search in common tags
        text = tag.get_text(strip=True)  # Extract visible text
        link = tag.get("href") if tag.name == "a" else None

        # Add the text and link to the articles list if relevant
        if keyword in text:  # Check if the keyword appears in the text
            articles.append({
                "text": text,
                "link": link if link else "No link available"
            })

    return articles


# Streamlit App
def main():
    st.title("Gujarati Newspaper Article Scraper")
    st.sidebar.header("Newspaper Selection")

    # Dropdown for selecting the newspaper
    newspaper = st.sidebar.selectbox(
        "Choose a Newspaper",
        ["Sandesh", "Divya Bhaskar", "Gujarat Samachar"]
    )

    # Keyword input field
    keyword = st.text_input("Enter a keyword (in any language):")

    # Newspaper URLs (base links)
    newspaper_urls = {
        "Sandesh": "https://www.sandesh.com",
        "Divya Bhaskar": "https://www.divyabhaskar.com",
        "Gujarat Samachar": "https://www.gujaratsamachar.com"
    }

    # Fetch and display results
    if st.button("Search"):
        if not keyword:
            st.warning("Please enter a keyword.")
        else:
            st.info(f"Searching articles from {newspaper} with keyword '{keyword}'...")
            url = newspaper_urls[newspaper]
            articles = scrape_general(url, keyword)

            if articles:
                st.success(f"Found {len(articles)} articles!")
                for idx, article in enumerate(articles, start=1):
                    st.write(f"### Article {idx}")
                    st.write(f"**Text**: {article['text']}")
                    st.write(f"**Link**: [Visit Article]({article['link']})" if article['link'] != "No link available" else "**Link**: No link available")
                    st.write("---")
            else:
                st.warning(f"No articles found for keyword '{keyword}' on {newspaper}.")

# Run the app
if __name__ == "__main__":
    main()

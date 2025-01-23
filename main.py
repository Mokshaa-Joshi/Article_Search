import streamlit as st
import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator

# Function to fetch article links based on keyword search for Gujarat Midday
def fetch_article_links(base_url, keyword):
    try:
        # Fetch the page content
        response = requests.get(base_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # List to hold article links and headlines
        links = []

        # Look for all <a> tags with href attribute
        for a in soup.find_all('a', href=True):
            # Check if keyword is in href or anchor text (case insensitive)
            if keyword.lower() in a.get('href', '').lower() or keyword.lower() in a.text.lower():
                href = a['href']
                # Ensure full URL if it's a relative path
                if not href.startswith("http"):
                    href = f"{base_url.rstrip('/')}/{href.lstrip('/')}"
                links.append((a.text.strip(), href))  # Store headline and link

        return links
    except Exception as e:
        st.error(f"An error occurred while fetching links: {e}")
        return []

# Function to extract article content and date
def extract_article(link):
    try:
        # Fetch the article page content
        response = requests.get(link)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the date of publication (adjust for Gujarat Midday's structure)
        date = soup.find('span', class_='time')
        article_date = date.get_text(strip=True) if date else "Date not found"

        # Extract the article content (body)
        content = soup.find('div', class_='article-detail')
        if content:
            article_text = "\n".join(p.get_text() for p in content.find_all('p'))
        else:
            paragraphs = soup.find_all('p')
            article_text = "\n".join(p.get_text() for p in paragraphs if p.get_text())

        return article_date, article_text if article_text else "No article content found."
    except Exception as e:
        return f"Error extracting article: {e}", ""

# Function to translate text to Gujarati
def translate_text(text, target_language="gu"):
    try:
        # Translate text to target language (Gujarati by default)
        translated = GoogleTranslator(source='auto', target=target_language).translate(text)
        return translated
    except Exception as e:
        st.error(f"Error translating article: {e}")
        return text

# Function to display the articles
def display_articles(links):
    if links:
        for headline, link in links:
            with st.expander(f"**{headline}**"):
                # Create a markdown link that opens in a new tab
                st.markdown(f"[Read Full Article]({link})", unsafe_allow_html=True)  # Link to the original article
                
                date, content = extract_article(link)
                st.write(f"**Published on:** {date}")
                
                if content:
                    st.write(f"**Article Content (Original):**\n{content}")
                    # Translate content if needed
                    translated_content = translate_text(content)
                    st.write(f"**Article Content (Translated):**\n{translated_content}")
                else:
                    st.warning(f"Article has no content.")
    else:
        st.warning("No articles found.")

# Streamlit app main function
def main():
    st.set_page_config(page_title="Gujarati News Article Finder", page_icon="📰")
    st.title("Gujarati News Article Finder")

    # Newspaper selection and keyword input
    newspaper = st.selectbox("Choose Newspaper", ["Gujarat Midday", "Divya Bhaskar", "Gujarat Samachar"])
    keyword = st.text_input("Enter keyword:")

    if st.button("Search Articles"):
        base_url = {
            "Gujarat Midday": "https://www.gujaratimidday.com/",
            "Divya Bhaskar": "https://www.divyabhaskar.com/",
            "Gujarat Samachar": "https://www.gujaratsamachar.com/"
        }[newspaper]

        with st.spinner("Searching..."):
            links = fetch_article_links(base_url, keyword)
            display_articles(links)

if __name__ == "__main__":
    main()

import streamlit as st
import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator

# Function to fetch article links
def fetch_article_links(base_url, keyword):
    try:
        # Fetch the page content
        response = requests.get(base_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        links = []
        # Look for all <a> tags with href attribute
        for a in soup.find_all('a', href=True):
            # Check if keyword is in href or anchor text (case insensitive)
            if keyword.lower() in a.get('href', '').lower() or keyword.lower() in a.text.lower():
                href = a['href']
                # Ensure full URL if it's a relative path
                if not href.startswith("http"):
                    href = f"{base_url.rstrip('/')}/{href.lstrip('/')}"
                links.append(href)

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

        # Extract the date of publication
        date = soup.find('h5')  # Replace 'h5' with the actual tag for the date
        article_date = date.get_text(strip=True) if date else "Date not found"

        # Extract the article content (body)
        content = soup.find('div', class_='article-body')  # Replace with actual class
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

# Main Streamlit app
def main():
    st.set_page_config(page_title="Gujarati News Scraper", page_icon="📰")
    st.title("Gujarati News Article Finder")

    # Sidebar for newspaper selection
    st.sidebar.header("Select a Newspaper")
    newspaper_options = {
        "Sandesh": "https://www.sandesh.com/",
        "Divya Bhaskar": "https://www.divyabhaskar.com/",
        "Gujarat Samachar": "https://www.gujaratsamachar.com/"
    }
    selected_newspaper = st.sidebar.selectbox("Choose a Newspaper", list(newspaper_options.keys()))

    # Keyword input
    keyword = st.text_input("Enter a keyword (in any language):")

    if st.button("Search Articles"):
        if keyword:
            # Detect language and translate keyword if necessary
            with st.spinner("Detecting keyword language..."):
                detected_language = GoogleTranslator(source='auto', target='en').translate(keyword)
                if detected_language == keyword:
                    st.info(f"Detected keyword in English: '{keyword}'")
                else:
                    st.info(f"Detected keyword in Gujarati: '{keyword}'")
                
                translated_keyword = keyword

            # Fetch articles from the selected newspaper
            with st.spinner(f"Searching for articles in {selected_newspaper}..."):
                base_url = newspaper_options[selected_newspaper]
                links = fetch_article_links(base_url, translated_keyword)

                if links:
                    st.success(f"Found {len(links)} articles:")
                    for i, link in enumerate(links, start=1):
                        st.write(f"**Article {i}:** [Link]({link})")

                        with st.spinner(f"Extracting content for Article {i}..."):
                            article_date, article_content = extract_article(link)
                            st.write(f"**Published on:** {article_date}")

                            if article_content:
                                st.write(f"**Original Content:**\n{article_content}")
                                translated_content = translate_text(article_content)
                                st.write(f"**Translated Content:**\n{translated_content}")
                            else:
                                st.warning("No content found for this article.")
                        st.write("---")
                else:
                    st.warning(f"No articles found with the keyword '{translated_keyword}'.")
        else:
            st.error("Please enter a keyword.")

if __name__ == "__main__":
    main()

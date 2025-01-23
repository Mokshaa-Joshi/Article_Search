import streamlit as st

import requests

from bs4 import BeautifulSoup

from urllib.parse import urljoin, urlparse



def normalize_url(url, base_url):

    if not url.startswith("http"):

        url = urljoin(base_url, url)

    

    parsed_url = urlparse(url)

    normalized_url = parsed_url._replace(query='', fragment='').geturl()

    

    return normalized_url



def fetch_article_links(base_url, keyword):

    try:

        response = requests.get(base_url)

        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')



        links = set()



        for a in soup.find_all('a', href=True):

            if keyword.lower() in a.get('href', '').lower() or keyword.lower() in a.text.lower():

                href = a['href']

                normalized_url = normalize_url(href, base_url)

                links.add((a.text.strip(), normalized_url))



        return list(links)

    except Exception as e:

        st.error(f"An error occurred while fetching links: {e}")

        return []



def extract_article(link):

    try:

        response = requests.get(link)

        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')



        date = soup.find('span', class_='time')

        article_date = date.get_text(strip=True) if date else "Date not found"



        content = soup.find('div', class_='article-detail')

        if content:

            article_text = "\n".join(p.get_text() for p in content.find_all('p'))

        else:

            paragraphs = soup.find_all('p')

            article_text = "\n".join(p.get_text() for p in paragraphs if p.get_text())



        return article_date, article_text if article_text else "No article content found."

    except Exception as e:

        return f"Error extracting article: {e}", ""



def display_articles(links):

    if links:

        seen_articles = set()



        for headline, link in links:

            if link not in seen_articles:

                with st.expander(f"**{headline}**"):

                    st.markdown(f"[Read Full Article]({link})", unsafe_allow_html=True)

                    

                    date, content = extract_article(link)

                    st.write(f"**Published on:** {date}")

                    

                    if content:

                        st.write(f"**Article Content:**\n{content}")

                    else:

                        st.warning(f"Article has no content.")

                

                seen_articles.add(link)

    else:

        st.warning("No articles found.")



def main():

    st.set_page_config(page_title="Gujarati News Article Finder", page_icon="📰")

    st.title("Gujarati News Article Finder")



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

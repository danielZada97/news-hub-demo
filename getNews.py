import requests
from bs4 import BeautifulSoup
import re
all_headlines = {}


def all_sites_headlines():
    global all_headlines
    with open('news_xml.txt', 'r') as xml_sites:
        for xml_url in xml_sites:
            print(f'{xml_url}')
            temp_dic=get_rss_headlines_with_links(xml_url)
            all_headlines.update(temp_dic)


def is_website_format(url):
    pattern = r"^(http|https)://([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})(/[a-zA-Z0-9_./-]*)?$"
    match = re.match(pattern, url)
    # If match is found, return True; otherwise, return False
    return bool(match)

def get_rss_headlines_with_links(xml_url):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    response = requests.get(xml_url, headers=headers)

    

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "xml")  # Use xml as the parser for RSS feeds
        items = soup.find_all("item")
        headlines_with_links = {}

        for item in items:
            headline = item.find("title").text
            guid_element = item.find("guid")
            link_element=item.find("link")
            if is_website_format(guid_element.text):
                link=guid_element.text
            elif is_website_format(link_element.text):
                link=link_element.text
            else :"link not found!"
            
            headlines_with_links[headline] = link

        return headlines_with_links
    else:
        print(f"Failed to fetch RSS feed from {xml_url}.")
        return {}

# Provide the direct URL to the XML RSS feed

xml_rss_url = "http://rss.cnn.com/rss/edition.rss"
all_headlines_with_links = get_rss_headlines_with_links(xml_rss_url)

if all_headlines_with_links:
    for index, (headline, link) in enumerate(all_headlines_with_links.items(), 1):
        print(f"{index}. {headline}: {link}")
else:
    print("No headlines found.")

#works for all RSS feeds for news sites

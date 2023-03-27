import os
import sys
import json
import datetime
import psycopg2
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from urllib.parse import urlparse, urljoin

timestamp = datetime.datetime.now()


def main(sitemap_url):

    # Download the sitemap content
    response = requests.get(sitemap_url)

    # Parse the sitemap XML
    root = ET.fromstring(response.content)

    urls = []
    for loc in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
        urls.append(loc.text)

    # Set up the PostgreSQL connection
    conn = psycopg2.connect(
        dbname=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'],
        host=os.environ['DB_HOST'],
        port=os.environ['DB_PORT']
    )
    cursor = conn.cursor()

    # Process each URL
    for url in urls:
        process_url(url, cursor, conn)

    # Close the PostgreSQL connection
    cursor.close()
    conn.close()


def process_url(url, cursor, conn):
    # Download the page content
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Scrape the data
    item = {}
    item['url'] = url
    item['title'] = soup.title.string if soup.title else None
    item['meta_description'] = soup.find('meta', attrs={'name': 'description'})['content'] if soup.find('meta', attrs={'name': 'description'}) else None
    item['h1'] = soup.h1.text if soup.h1 else None
    item['h2'] = json.dumps([h2.text for h2 in soup.find_all('h2')])
    item['internal_links'] = [a['href'] for a in soup.find_all('a', href=True) if urlparse(a['href']).netloc == urlparse(url).netloc]
    item['external_links'] = json.dumps([a['href'] for a in soup.find_all('a', href=True) if urlparse(a['href']).netloc != urlparse(url).netloc])
    item['url_length'] = len(url)
    item['title_length'] = len(item['title']) if item['title'] else None
    item['meta_description_length'] = len(item['meta_description']) if item['meta_description'] else None
    item['h1_length'] = len(item['h1']) if item['h1'] else None
    item['h2_length'] = json.dumps([len(i) for i in item['h2'].split('"')])
    item['count_paragraphs'] = len(soup.find_all('p'))
    item['response_time'] = response.elapsed.total_seconds()
    item['status'] = response.status_code
    item['word_count'] = len(soup.get_text().split())
    item['page_size'] = len(response.content)
    item['text_ratio'] = item['word_count'] / item['page_size']
    item['canonical_url'] = soup.find('link', attrs={'rel': 'canonical'})['href'] if soup.find('link', attrs={'rel': 'canonical'}) else None
    item['meta_robots'] = soup.find('meta', attrs={'name': 'robots'})['content'] if soup.find('meta', attrs={'name': 'robots'}) else None
    item['image_alt_attributes'] = json.dumps([img['alt'] if 'alt' in img.attrs else None for img in soup.find_all('img')])
    item['structured_data'] = json.dumps([script.string for script in soup.find_all('script', attrs={'type': 'application/ld+json'})])
    item['broken_links'] = []  # This requires additional logic to identify broken links
    item['language_tags'] = soup.html['lang'] if 'lang' in soup.html.attrs else None
    item['timestamp'] = timestamp

    # Save the data to the
    save_to_postgresql(item, cursor, conn)

def save_to_postgresql(item, cursor, conn):
    query = """
        INSERT INTO seo_data (
            url, title, meta_description, h1, h2, internal_links, external_links,
            url_length, title_length, meta_description_length, h1_length, h2_length, count_paragraphs,
            response_time, status, word_count, page_size, text_ratio, canonical_url,
            meta_robots, image_alt_attributes, structured_data, broken_links, language_tags, timestamp
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """

    data = (
        item['url'],
        item['title'],
        item['meta_description'],
        item['h1'],
        item['h2'],
        item['internal_links'],
        item['external_links'],
        item['url_length'],
        item['title_length'],
        item['meta_description_length'],
        item['h1_length'],
        item['h2_length'],
        item['count_paragraphs'],
        item['response_time'],
        item['status'],
        item['word_count'],
        item['page_size'],
        item['text_ratio'],
        item['canonical_url'],
        item['meta_robots'],
        item['image_alt_attributes'],
        item['structured_data'],
        item['broken_links'],
        item['language_tags'],
        item['timestamp']
    )

    cursor.execute(query, data)
    conn.commit()

if __name__ == '__main__':
    sitemap_url = sys.argv[1]
    main(sitemap_url)

import os
import sys
import datetime
import psycopg2
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from utilities import *
from termcolor import colored

timestamp = datetime.datetime.now()


def main(sitemap_url):

    response = requests.get(sitemap_url)
    root = ET.fromstring(response.content)

    urls = []
    for loc in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
        urls.append(loc.text)

    conn = psycopg2.connect(
        dbname=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASS'],
        host=os.environ['DB_HOST'],
        port=os.environ['DB_PORT']
    )
    cursor = conn.cursor()

    items = []
    alert_names = None
    for url in tqdm(urls, desc="Processing URLs", unit="URL", ncols=80):
        item, alert_names = process_url(url, cursor, conn)
        items.append(item)

    cursor.close()
    conn.close()

    print_summary_report(items, alert_names)


def process_url(url, cursor, conn):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    item = {}
    item['url'] = url
    item['title'] = extract_title(soup)
    item['meta_description'] = extract_meta_description(soup)
    item['h1'] = extract_h1(soup)
    item['h2'] = extract_h2(soup)
    item['internal_links'] = extract_internal_links(soup, url)
    item['external_links'] = extract_external_links(soup, url)
    item['count_internal_links'] = count_internal_links(item['internal_links'])
    item['count_external_links'] = count_external_links(item['external_links'])
    item['url_length'] = extract_url_length(url)
    item['title_length'] = extract_title_length(item['title'])
    item['meta_description_length'] = extract_meta_description_length(item['meta_description'])
    item['meta_keyword'] = extract_meta_keywords(soup)
    item['h1_length'] = extract_h1_length(item['h1'])
    item['h2_length'] = extract_h2_length(item['h2'])
    item['count_paragraphs'] = extract_count_paragraphs(soup)
    item['response_time'] = extract_response_time(response)
    item['status'] = extract_status(response)
    item['word_count'] = extract_word_count(soup)
    item['page_size'] = extract_page_size(response)
    item['text_ratio'] = extract_text_ratio(item['word_count'], item['page_size'])
    item['canonical_url'] = extract_canonical_url(soup)
    item['meta_robots'] = extract_meta_robots(soup)
    item['image_alt_attributes'] = extract_image_alt_attributes(soup)
    item['structured_data'] = extract_structured_data(soup)
    item['language_tags'] = extract_language_tags(soup)
    item['timestamp'] = timestamp

    alerts, alert_names = generate_seo_alerts(item)
    item.update(alerts)

    save_to_postgresql(item, cursor, conn)

    return item, alert_names


def save_to_postgresql(item, cursor, conn):
    columns = ', '.join(item.keys())
    placeholders = ', '.join(['%s'] * len(item))
    query = f"""
        INSERT INTO seo_data ({columns})
        VALUES ({placeholders});
    """
    data = tuple(item.values())
    cursor.execute(query, data)
    conn.commit()


def print_summary_report(items, alert_names):
    total_urls = len(items)
    urls_with_alerts = sum(1 for item in items if item['has_alert'])
    urls_without_alerts = total_urls - urls_with_alerts

    print(colored(f"\nTotal URLs: {total_urls}", "green"))
    print(colored(f"URLs without alerts: {urls_without_alerts}", "blue"))
    print(colored(f"URLs with alerts: {urls_with_alerts}", "red"))

    print(colored("\nAlerts breakdown:", "cyan"))
    for alert_type in alert_names:
        if alert_type != 'has_alert':
            alert_count = sum(1 for item in items if item[alert_type])
            print(colored(f"\t{alert_type}: {alert_count}", "yellow"))

    print(colored("\nSummary report completed.", "magenta"))


if __name__ == '__main__':
    sitemap_url = sys.argv[1]
    main(sitemap_url)

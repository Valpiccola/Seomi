import re
import json
from urllib.parse import urlparse
from urllib.parse import urljoin


def extract_title(soup):
    return soup.title.string if soup.title else None


def extract_meta_description(soup):
    meta_tag = soup.find('meta', attrs={'name': 'description'})
    return meta_tag['content'] if meta_tag else None


def extract_h1(soup):
    return soup.h1.text if soup.h1 else None


def extract_h2(soup):
    return json.dumps([h2.text for h2 in soup.find_all('h2')])


def extract_internal_links(soup, url):
    internal_links = [urljoin(url, a['href']) for a in soup.find_all('a', href=True) if urlparse(urljoin(url, a['href'])).netloc == urlparse(url).netloc]
    return json.dumps(internal_links)


def extract_external_links(soup, url):
    external_links = [urljoin(url, a['href']) for a in soup.find_all('a', href=True) if urlparse(urljoin(url, a['href'])).netloc != urlparse(url).netloc]
    return json.dumps(external_links)


def count_internal_links(internal_links_json):
    internal_links = json.loads(internal_links_json)
    return len(set(internal_links))


def count_external_links(external_links_json):
    external_links = json.loads(external_links_json)
    return len(set(external_links))


def extract_url_length(url):
    return len(url)


def extract_title_length(title):
    return len(title) if title else None


def extract_meta_description_length(meta_description):
    return len(meta_description) if meta_description else None


def extract_h1_length(h1):
    return len(h1) if h1 else None


def extract_h2_length(h2_json):
    return json.dumps([len(i) for i in json.loads(h2_json)])


def extract_count_paragraphs(soup):
    return len(soup.find_all('h2'))


def extract_response_time(response):
    return response.elapsed.total_seconds()


def extract_status(response):
    return response.status_code


def extract_word_count(soup):
    for s in soup(['script', 'style']):
        s.decompose()
    words = re.findall(r'\w+', soup.get_text())
    return len(words)


def extract_page_size(response):
    return len(response.content)


def extract_text_ratio(word_count, page_size):
    return word_count / page_size


def extract_canonical_url(soup):
    canonical_tag = soup.find('link', attrs={'rel': 'canonical'})
    return canonical_tag['href'] if canonical_tag else None


def extract_meta_robots(soup):
    meta_robots_tag = soup.find('meta', attrs={'name': 'robots'})
    return meta_robots_tag['content'] if meta_robots_tag else None


def extract_image_alt_attributes(soup):
    return json.dumps([img['alt'] if 'alt' in img.attrs else None for img in soup.find_all('img')])


def extract_structured_data(soup):
    return json.dumps([script.string for script in soup.find_all('script', attrs={'type': 'application/ld+json'})])


def extract_language_tags(soup):
    return soup.html['lang'] if 'lang' in soup.html.attrs else None


def extract_meta_keywords(soup):
    meta_tag = soup.find('meta', attrs={'name': 'keyword'})
    return meta_tag['content'] if meta_tag and 'content' in meta_tag.attrs else None


def generate_seo_alerts(item):
    alerts = {
        'alert_missing_title': item['title'] is None,
        'alert_long_title': (item['title_length'] < 55 or item['title_length'] > 60) if item['title_length'] is not None else False,
        'alert_missing_meta_description': item['meta_description'] is None,
        'alert_long_meta_description': (item['meta_description_length'] < 155 or item['meta_description_length'] > 160) if item['meta_description_length'] is not None else False,
        'alert_missing_h1': item['h1'] is None,
        'alert_incorrect_canonical_url': item['canonical_url'] is None or item['canonical_url'] != item['url'],
        'alert_missing_image_alt_attributes': any(alt is None for alt in json.loads(item['image_alt_attributes'])),
        'alert_missing_language_tag': item['language_tags'] is None,
        'alert_low_text_ratio': item['text_ratio'] < 0.15,
        'alert_no_meta_robots_or_incorrect_directives': item['meta_robots'] is None or 'noindex' in item['meta_robots'].lower() or 'nofollow' in item['meta_robots'].lower(),
    }
    alerts['has_alert'] = any(alerts.values())
    return alerts

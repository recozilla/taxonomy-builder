import argparse
import requests
import xml.etree.ElementTree as ET
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from collections import defaultdict


def fetch(url):
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.text


def parse_sitemap(xml_text):
    tree = ET.fromstring(xml_text)
    urls = []
    # sitemap index
    for loc in tree.findall('.//{*}sitemap/{*}loc'):
        child_xml = fetch(loc.text)
        urls.extend(parse_sitemap(child_xml))
    # regular sitemap
    for loc in tree.findall('.//{*}url/{*}loc'):
        urls.append(loc.text)
    return urls


def get_sitemap_urls(domain):
    sitemap_url = urljoin(domain, '/sitemap.xml')
    xml_text = fetch(sitemap_url)
    return parse_sitemap(xml_text)


def extract_text(url):
    html = fetch(url)
    soup = BeautifulSoup(html, 'html.parser')
    return soup.get_text(separator=' ', strip=True)


def identify_products(page_text):
    products = []
    lines = page_text.split('\n')
    for line in lines:
        lower = line.lower()
        if 'product' in lower or 'solution' in lower:
            products.append(line.strip())
    return products


def main(domain):
    if not domain.startswith('http'):  # add scheme if missing
        domain = 'https://' + domain
    urls = get_sitemap_urls(domain)
    product_mentions = defaultdict(list)
    for url in urls:
        try:
            text = extract_text(url)
        except Exception as e:
            print(f'failed to fetch {url}: {e}')
            continue
        candidates = identify_products(text)
        for candidate in candidates:
            product_mentions[candidate].append(url)

    print('Found products/solutions:')
    for prod, pages in product_mentions.items():
        print(f'- {prod} (mentioned on {len(pages)} pages)')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Build a taxonomy of products/solutions from a website sitemap.')
    parser.add_argument('domain', help='Domain name, e.g., example.com or https://example.com')
    args = parser.parse_args()
    main(args.domain)

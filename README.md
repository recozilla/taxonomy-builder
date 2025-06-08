# taxonomy-builder

This repository contains a simple command-line tool that crawls a website's sitemap and attempts to identify product and solution references on its pages. It collects these mentions and prints a basic taxonomy of the products and solutions found.

## Usage

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the crawler with a domain:
   ```bash
   python main.py example.com
   ```

The tool fetches `/sitemap.xml`, follows any referenced sitemaps, downloads each page, and searches for lines containing the words `product` or `solution`. The results are printed with a count of the pages mentioning each entry.


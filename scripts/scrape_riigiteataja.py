import requests
from bs4 import BeautifulSoup
import json
import re
import os
import time

# --- 1. Clean filename ---
def sanitize_filename(name, max_length=100):
    name = re.sub(r'[\\/*?:"<>|]', '', name)
    name = name.replace(' ', '_')
    return name[:max_length]

# --- 2. Scrape one law ---
def scrape_law(url, output_dir):
    # 🛡️ Add user-agent header to avoid getting blocked
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/117.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract title
    title = soup.find('h1')
    title_text = title.get_text(strip=True) if title else 'untitled_law'

    # Extract content
    main_div = soup.find('div', id='article-content')
    if not main_div:
        print(f"[!] Content not found in URL: {url}")
        return

    main_text = main_div.get_text(separator='\n', strip=True)

    # Prepare filename and path
    safe_title = sanitize_filename(title_text)
    filename = os.path.join(output_dir, f"{safe_title}.json")

    # ✅ Skip if already scraped
    if os.path.exists(filename):
        print(f"[!] Skipping already scraped: {filename}")
        return

    # Build data
    law_data = {
        'url': url,
        'title': title_text,
        'text': main_text
    }

    # Save JSON file
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(law_data, f, ensure_ascii=False, indent=2)

    print(f"[✓] Saved: {filename}")

# --- 3. Main loop to scrape multiple laws ---
if __name__ == '__main__':
    law_urls = [
        'https://www.riigiteataja.ee/akt/112112023014',
        'https://www.riigiteataja.ee/akt/109012024001',
        'https://www.riigiteataja.ee/akt/103012024003',
        'https://www.riigiteataja.ee/akt/104032024005',
        'https://www.riigiteataja.ee/akt/118012024002',
        'https://www.riigiteataja.ee/akt/106042024002',
        'https://www.riigiteataja.ee/akt/115022024001',
        'https://www.riigiteataja.ee/akt/107012024002',
        'https://www.riigiteataja.ee/akt/113012024003',
        'https://www.riigiteataja.ee/akt/116012024004'
    ]

    # Set output folder relative to script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.abspath(os.path.join(script_dir, '..', 'data', 'raw_laws'))
    os.makedirs(output_dir, exist_ok=True)

    # 🔁 Loop with delay
    for i, url in enumerate(law_urls, 1):
        print(f"\n[{i}/{len(law_urls)}] Scraping: {url}")
        try:
            scrape_law(url, output_dir)
            time.sleep(4)  # ⏳ Wait between requests
        except Exception as e:
            print(f"[X] Error scraping {url}: {e}")
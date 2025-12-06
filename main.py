import requests
import time
import random
from duckduckgo_search import DDGS

# 1. SETUP: What are we looking for?
KEYWORDS = ["luxury watch store", "custom jewelry", "electric bike shop", "designer furniture"]
OUTPUT_FILE = "leads.md"

def audit_site(url):
    try:
        # Pretend to be a real person on Chrome
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        start = time.time()
        response = requests.get(url, headers=headers, timeout=10)
        duration = round(time.time() - start, 2)
        
        if response.status_code == 200:
            html = response.text.lower()
            # Check for Facebook Pixel (fbevents.js)
            has_pixel = 'fbevents.js' in html
            
            # THE LOGIC: If they have a Pixel (Spending money) AND are slow (Wasting money)
            if has_pixel and duration > 3.0:
                return f"| {url} | {duration}s | CRITICAL (Slow) |"
    except:
        return None
    return None

def run_hunter():
    print("--- 🤖 HUNTER BOT STARTED ---")
    unique_domains = set()
    
    # 2. SEARCH PHASE
    with DDGS() as ddgs:
        for keyword in KEYWORDS:
            print(f"Searching: {keyword}...")
            # We look for Shopify stores specifically
            results = ddgs.text(f'site:myshopify.com "{keyword}"', max_results=5)
            if results:
                for r in results:
                    unique_domains.add(r['href'])
            time.sleep(2)

    # 3. AUDIT PHASE
    print(f"Auditing {len(unique_domains)} stores...")
    found_leads = []
    
    for url in unique_domains:
        result = audit_site(url)
        if result:
            found_leads.append(result)
            print(f"Found: {url}")
        time.sleep(1)

    # 4. SAVE PHASE
    if found_leads:
        with open(OUTPUT_FILE, "a") as f:
            f.write(f"\n\n### Scan: {time.strftime('%Y-%m-%d')}\n")
            f.write("| URL | Speed | Status |\n|---|---|---|\n")
            for lead in found_leads:
                f.write(lead + "\n")
    
    print("--- DONE ---")

if __name__ == "__main__":
    run_hunter()

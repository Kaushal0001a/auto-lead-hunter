import requests
import time
import random
from duckduckgo_search import DDGS

KEYWORDS = ["luxury watch store", "custom jewelry", "electric bike shop"]
OUTPUT_FILE = "leads.md"

def audit_site(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        start = time.time()
        response = requests.get(url, headers=headers, timeout=10)
        duration = round(time.time() - start, 2)
        
        if response.status_code == 200:
            # TEST MODE: We save EVERYTHING just to prove it works
            return f"| {url} | {duration}s | Scanned (Test) |"
    except:
        return None
    return None

def run_hunter():
    print("--- 🤖 HUNTER BOT STARTED (TEST MODE) ---")
    unique_domains = set()
    
    # 1. SEARCH
    with DDGS() as ddgs:
        for keyword in KEYWORDS:
            print(f"Searching: {keyword}...")
            # Search for Shopify stores
            results = ddgs.text(f'site:myshopify.com "{keyword}"', max_results=5)
            if results:
                for r in results:
                    unique_domains.add(r['href'])
            time.sleep(1)

    # 2. AUDIT
    print(f"Auditing {len(unique_domains)} stores...")
    found_leads = []
    
    for url in unique_domains:
        result = audit_site(url)
        if result:
            found_leads.append(result)
            print(f"Saved: {url}")
        time.sleep(1)

    # 3. SAVE
    # We force it to write the file no matter what
    with open(OUTPUT_FILE, "a") as f:
        f.write(f"\n\n### Test Scan: {time.strftime('%Y-%m-%d')}\n")
        f.write("| URL | Speed | Status |\n|---|---|---|\n")
        for lead in found_leads:
            f.write(lead + "\n")
    
    print("--- DONE ---")

if __name__ == "__main__":
    run_hunter()

import requests
import time

# WE GIVE IT A MAP INSTEAD OF SEARCHING BLINDLY
TARGETS = [
    "https://www.gymshark.com",
    "https://www.colourpop.com",
    "https://www.fashionnova.com",
    "https://www.allbirds.com",
    "https://kyliecosmetics.com",
    "https://www.mvmt.com"
]
OUTPUT_FILE = "leads.md"

def audit_site(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        start = time.time()
        response = requests.get(url, headers=headers, timeout=10)
        duration = round(time.time() - start, 2)
        
        if response.status_code == 200:
            html = response.text.lower()
            has_pixel = 'fbevents.js' in html
            
            # Label the result
            status = "Good"
            if duration > 2.0:
                status = "SLOW (Potential Lead)"
            
            return f"| {url} | {duration}s | {status} |"
    except:
        return f"| {url} | Error | Failed |"
    return None

def run_hunter():
    print("--- 🤖 HUNTER BOT STARTED (DIRECT MODE) ---")
    
    found_leads = []
    
    for url in TARGETS:
        print(f"Auditing: {url}...")
        result = audit_site(url)
        if result:
            found_leads.append(result)
        time.sleep(1)

    # WRITE TO FILE
    with open(OUTPUT_FILE, "a") as f:
        f.write(f"\n\n### Audit Report: {time.strftime('%Y-%m-%d %H:%M')}\n")
        f.write("| URL | Speed | Status |\n|---|---|---|\n")
        for lead in found_leads:
            f.write(lead + "\n")
    
    print("--- DONE ---")

if __name__ == "__main__":
    run_hunter()

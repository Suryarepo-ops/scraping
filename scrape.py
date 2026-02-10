import requests
from bs4 import BeautifulSoup
import re

def scrape_company_info(url):
    """
    Scrapes company information (Name, Email, Phone) from the given URL.
    """
    # Use headers to mimic a real browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        soup = BeautifulSoup(response.content, 'lxml')
        
        # --- SELECTORS (Placeholders - UPDATE THESE based on the specific website) ---
        # Example: company_name = soup.select_one('h1.company-title').text.strip()
        
        # 1. Company Name
        # Heuristic: Often in the <title> or an <h1> tag
        company_name = soup.title.text.strip() if soup.title else "N/A"
        # specific_selector = soup.select_one('h1') # Uncomment and update
        # if specific_selector: company_name = specific_selector.text.strip()

        # 2. Email Address
        # Heuristic: Search for mailto: links or regex in text
        email = "N/A"
        mailto_link = soup.select_one('a[href^="mailto:"]')
        if mailto_link:
            email = mailto_link['href'].replace('mailto:', '').strip()
        else:
            # Fallback regex search
            emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', soup.text)
            if emails:
                email = emails[0] # Take the first one found

        # 3. Phone Number
        # Heuristic: Search for tel: links or regex
        phone = "N/A"
        tel_link = soup.select_one('a[href^="tel:"]')
        if tel_link:
            phone = tel_link['href'].replace('tel:', '').strip()
        else:
            # Fallback regex for various phone formats (basic example)
            # Matches: (123) 456-7890, 123-456-7890, +1-123-456-7890
            phones = re.findall(r'(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}', soup.text)
            if phones:
                # Need to post-process regex matches as they return tuples
                # This is a simplified example
                phone = "Found potential numbers, need specific formatting logic"

        return {
            "url": url,
            "company_name": company_name,
            "email": email,
            "phone": phone
        }

    except requests.RequestException as e:
        print(f"Error scraping {url}: {e}")
        return None

if __name__ == "__main__":
    # --- CONFIGURATION ---
    TARGET_URL = "https://example.com"  # <--- REPLACE THIS WITH YOUR TARGET URL
    
    print(f"Scraping {TARGET_URL}...")
    data = scrape_company_info(TARGET_URL)
    
    if data:
        print("\nScraped Information:")
        for key, value in data.items():
            print(f"{key.replace('_', ' ').capitalize()}: {value}")

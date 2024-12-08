import requests
from bs4 import BeautifulSoup
import re
import argparse

def fetch_html(url):
    """Fetches the HTML content of a given URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None

def extract_emails(html):
    """Extracts email addresses from the HTML content."""
    return re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", html)

def extract_phone_numbers(html):
    """Extracts phone numbers from the HTML content."""
    return re.findall(r"\+?\d[\d -]{8,15}\d", html)

def extract_social_links(html):
    """Extracts social media profile links from the HTML content."""
    soup = BeautifulSoup(html, "html.parser")
    links = []
    for anchor in soup.find_all("a", href=True):
        if any(domain in anchor["href"] for domain in ["facebook.com", "twitter.com", "linkedin.com", "instagram.com"]):
            links.append(anchor["href"])
    return links

def main():
    parser = argparse.ArgumentParser(description="OSINT Analyzer by Yuvaraj")
    parser.add_argument("-u", "--url", required=True, help="Target website URL")
    args = parser.parse_args()

    html = fetch_html(args.url)
    if not html:
        return

    print("\n--- OSINT Results ---")
    emails = extract_emails(html)
    print(f"Emails Found: {emails}")

    phone_numbers = extract_phone_numbers(html)
    print(f"Phone Numbers Found: {phone_numbers}")

    social_links = extract_social_links(html)
    print(f"Social Media Links Found: {social_links}")

if __name__ == "__main__":
    main()
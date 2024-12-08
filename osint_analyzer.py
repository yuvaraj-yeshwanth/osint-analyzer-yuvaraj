import requests
from bs4 import BeautifulSoup
import re
import argparse


def fetch_html(url):
    """Fetch the HTML content of a given URL."""
    try:
        # Secure request without token or authentication
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None


def extract_emails(html):
    """Extract email addresses from the given HTML."""
    return re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", html)


def extract_phone_numbers(html):
    """Extract phone numbers from the HTML."""
    return re.findall(r"\+?\d[\d -]{8,15}\d", html)


def extract_social_links(html):
    """Extract social media profile links from the given HTML."""
    soup = BeautifulSoup(html, "html.parser")
    links = []
    for anchor in soup.find_all("a", href=True):
        if any(domain in anchor["href"] for domain in ["facebook.com", "twitter.com", "linkedin.com", "instagram.com"]):
            links.append(anchor["href"])
    return links


def main():
    parser = argparse.ArgumentParser(description="OSINT Analyzer by Yuvaraj")
    parser.add_argument(
        "-u", "--url", required=True, help="Enter the target website URL"
    )
    args = parser.parse_args()

    # Fetch data securely without a token
    html_content = fetch_html(args.url)
    if not html_content:
        print("Could not fetch content. Exiting.")
        return

    print("\n--- OSINT Analysis Results ---")
    emails = extract_emails(html_content)
    print(f"Extracted Emails: {emails}")

    phone_numbers = extract_phone_numbers(html_content)
    print(f"Extracted Phone Numbers: {phone_numbers}")

    social_links = extract_social_links(html_content)
    print(f"Extracted Social Media Links: {social_links}")


if __name__ == "__main__":
    main()


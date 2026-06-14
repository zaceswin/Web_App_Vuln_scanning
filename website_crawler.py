import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

class Crawler:
    def __init__(self, base_url):
        self.base_url = base_url
        self.visited = set()
        self.target_links = set()

    def get_forms(self, url):
        """Extracts all forms from a given URL."""
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        return soup.find_all("form")

    def crawl(self, url=None):
        if url is None:
            url = self.base_url

        if url in self.visited or not url.startswith(self.base_url):
            return

        print(f"[+] Crawling: {url}")
        self.visited.add(url)

        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")

            # Extract Links
            for link in soup.find_all("a", href=True):
                full_url = urljoin(url, link["href"])
                self.crawl(full_url)
                
            # Extract Forms (to be passed to the Injector later)
            forms = self.get_forms(url)
            for form in forms:
                print(f"    [!] Found form at {url} with action {form.get('action')}")
                
        except Exception as e:
            print(f"[-] Could not crawl {url}: {e}")

# Usage
crawler = Crawler("http://localhost/dvwa")
crawler.crawl()

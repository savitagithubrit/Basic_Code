from bs4 import BeautifulSoup

import requests

class BaseScraper:
    def __init__(self, url: str, headers: dict = None):
        self.url = url

        #  Default headers
        default_headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/142.0.0.0 Safari/537.36"
            )
        }

        #  Merge headers if user provided
        if headers:
            default_headers.update(headers)
        self.headers = default_headers

        # Fetch webpage
        self.web = requests.get(self.url, headers=self.headers)
        print("Status Code:", self.web.status_code)

        if self.web.status_code == 200:
            self.soup = BeautifulSoup(self.web.content, "html.parser")
        else:
            raise Exception(f"Failed to fetch webpage. Status: {self.web.status_code}")
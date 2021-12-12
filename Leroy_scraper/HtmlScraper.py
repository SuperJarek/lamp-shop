import requests
from lxml import html


class HtmlScraper:
    @staticmethod
    def get_html_page_tree(url):
        page = requests.request(
            'GET', url, headers=None, timeout=15, verify=False
        )
        return html.fromstring(page.content)

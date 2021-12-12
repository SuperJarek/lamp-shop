import os
import requests
import json
import shutil

from HtmlScraper import HtmlScraper
from LeroyItemScraper import LeroyItemScraper


class LeroyScraper:
    ROOT_SHOP_URL = 'https://www.leroymerlin.pl/'

    PRODUCT_LINKS_SELECTOR = '//div[@class="product "]//a[@class="url"]/@href'
    NEXT_PAGE_SELECTOR = '(//div[@class="paging"]//a[@class="next "]/@href)[1]'

    @staticmethod
    def scrap(uri, max_items, results_dir):
        """
        Scraps items from all of the subsequent shop pages starting from the provided link
        :param results_dir: directory to which results will be written
        :param max_items: max number of items that will be downloaded
        :param uri: link to a starting item list page in Leroy, eg. https://www.leroymerlin.pl/szukaj-produkty,fw956,strona-1.html?q=lampa
                    Parsing will go from that page on.
        """
        items = []
        items_links = LeroyScraper.get_items_links(uri, max_items)
        for link in items_links:
            items.append(LeroyItemScraper.get_item(link))
        LeroyScraper.save_to_disc(items, results_dir)

    @staticmethod
    def get_items_links(list_uri, max_items):
        all_links = []
        current_page_uri = list_uri
        is_last_page = False

        while not is_last_page:
            page_tree = HtmlScraper.get_html_page_tree(current_page_uri)
            all_links += LeroyScraper.extract_item_links_from_page(page_tree)
            current_page_uri = LeroyScraper.extract_next_page_uri(page_tree)
            if not current_page_uri or len(all_links) > max_items:
                is_last_page = True
        return all_links[0:max_items]

    @staticmethod
    def save_to_disc(items, path):
        if not os.path.exists(path):
            os.mkdir(path)
        LeroyScraper.save_metadata_to_disc(items, path + '\\items_data.json')
        #LeroyScraper.save_images_to_disc(items, path + '\\images')

    @staticmethod
    def save_metadata_to_disc(items, path):
        with open(path, 'w', encoding='utf-8') as file:
            file.write(json.dumps([item_json.__dict__ for item_json in items], ensure_ascii=False).encode('utf8').decode())

    @staticmethod
    def save_images_to_disc(items, directory_path):
        if not os.path.exists(directory_path):
            os.mkdir(directory_path)
        for item in items:
            r = requests.get(item.photo_uri, stream=True)
            with open(directory_path + '\\' + item.id + '.' + item.photo_uri.split(".")[-1], 'wb') as f:
                shutil.copyfileobj(r.raw, f)

    @staticmethod
    def extract_item_links_from_page(items_page_tree):
        locations = items_page_tree.xpath(LeroyScraper.PRODUCT_LINKS_SELECTOR)
        return list(map(lambda location: LeroyScraper.ROOT_SHOP_URL + location, locations))

    @staticmethod
    def extract_next_page_uri(items_page_tree):
        location = items_page_tree.xpath(LeroyScraper.NEXT_PAGE_SELECTOR)
        if len(location) != 0:
            return LeroyScraper.ROOT_SHOP_URL + items_page_tree.xpath(LeroyScraper.NEXT_PAGE_SELECTOR)[0]
        return None


if __name__ == '__main__':
    items_list_uri = "https://www.leroymerlin.pl/szukaj.html?q=lampa&sprawdz=true"
    max_items = 500
    results_dir = "G:\\Projects\\Scraper_Leroy\\downloaded"

    LeroyScraper.scrap(items_list_uri, max_items, results_dir)
    print('Done! \nResults in ' + results_dir)

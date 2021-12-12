from HtmlScraper import HtmlScraper
from ShoppingItem import ShoppingItem


class LeroyItemScraper:

    # SITE SPECIFIC SELECTORS
    ITEM_NAME_SELECTOR = '//div[@class="product-title"]/h1/text()'

    ITEM_ID_SELECTOR = '//meta[@property="product:retailer_part_no"]/@content'

    ITEM_PHO_URI_SELECTOR = '//div[@class="product-gallery"]/div[@class="photo-container"]//a/img[@class="custom-attrs"]/@src'
    ITEM_PHOTOS_URI_SELECTOR = '//div[@class="swiper-wrapper"]/div/a/@data-src-large'

    ITEM_PRICE_SELECTOR = '//div[@class="prices-top"]//span/@data-price'

    ITEM_DESCRIPTION_SELECTOR_1 = '//div[@class="product-info "]//span[@class="description"]/text()'
    ITEM_DESCRIPTION_SELECTOR_2 = '//div[@class="product-info hidden"]//span[@class="description"]/text()'

    PRODUCT_ATTRIBUTES_SELECTOR = '//table[@class="product-attributes-list"]//tr[@class="item-row"]'
    ATTRIBUTE_NAME_SELECTOR = './td[@class="item"]/text()'
    ATTRIBUTE_VALUE_SELECTOR_1 = './td[@class="value item"]/text()'
    ATTRIBUTE_VALUE_SELECTOR_2 = './td[@class="value item"]/a/text()'
    
    ITEM_CATEGORIES_SELECTOR = '//div[@class="breadcrumb-content"]/div[@class="breadcrumb-item"]/a/@title'
    ##

    @staticmethod
    def get_item(item_uri):
        page_tree = HtmlScraper.get_html_page_tree(item_uri)
        item = ShoppingItem()

        item.name = LeroyItemScraper.get_item_name(page_tree)
        item.price_pln = LeroyItemScraper.get_item_price(page_tree)
        item.description = LeroyItemScraper.get_item_description(page_tree)
        item.id = LeroyItemScraper.get_item_id(page_tree)
        item.main_photo_uri = LeroyItemScraper.get_photo_uri(page_tree)
        item.photos = LeroyItemScraper.get_all_photos(page_tree)
        item.categories = LeroyItemScraper.get_categories(page_tree)

        attributes_table_rows = page_tree.xpath(LeroyItemScraper.PRODUCT_ATTRIBUTES_SELECTOR)
        item.attributes = LeroyItemScraper.get_item_attributes(attributes_table_rows)

        return item

    @staticmethod
    def get_all_photos(page_tree):
        result = []
        cat_search = page_tree.xpath(LeroyItemScraper.ITEM_PHOTOS_URI_SELECTOR)
        for cat in cat_search:
            result.append(str(cat).strip())
        return result

    @staticmethod
    def get_categories(page_tree):
        result = []
        cat_search = page_tree.xpath(LeroyItemScraper.ITEM_CATEGORIES_SELECTOR)
        for cat in cat_search:
            result.append(str(cat).strip())
        return result[1:]

    @staticmethod
    def get_item_description(page_tree):
        try:
            attribute_value_search = page_tree.xpath(LeroyItemScraper.ITEM_DESCRIPTION_SELECTOR_1)
            if len(attribute_value_search) is 0:
                return str(page_tree.xpath(LeroyItemScraper.ITEM_DESCRIPTION_SELECTOR_2)[0]).strip()
            else:
                return str(attribute_value_search[0]).strip()
        except IndexError:
            return ""

    @staticmethod
    def get_photo_uri(page_tree):
        try:
            return str(page_tree.xpath(LeroyItemScraper.ITEM_PHO_URI_SELECTOR)[0]).strip()
        except IndexError:
            return ""

    @staticmethod
    def get_item_id(page_tree):
        try:
            return str(page_tree.xpath(LeroyItemScraper.ITEM_ID_SELECTOR)[0]).strip()
        except IndexError:
            return ""

    @staticmethod
    def get_item_price(page_tree):
        try:
            return str(page_tree.xpath(LeroyItemScraper.ITEM_PRICE_SELECTOR)[0]).strip()
        except IndexError:
            return ""

    @staticmethod
    def get_item_name(page_tree):
        try:
            return str(page_tree.xpath(LeroyItemScraper.ITEM_NAME_SELECTOR)[0]).strip()
        except IndexError:
            return ""

    @staticmethod
    def get_item_attributes(attributes_table_rows):
        attributes = {}
        for attribute_row_tree in attributes_table_rows:
            try:
                attribute_name = str(attribute_row_tree.xpath(LeroyItemScraper.ATTRIBUTE_NAME_SELECTOR)[0]).strip()
                attribute_value_search = attribute_row_tree.xpath(LeroyItemScraper.ATTRIBUTE_VALUE_SELECTOR_2)
                if len(attribute_value_search) is 0:
                    attribute_value = str(attribute_row_tree.xpath(LeroyItemScraper.ATTRIBUTE_VALUE_SELECTOR_1)[0]).strip()
                else:
                    attribute_value = str(attribute_value_search[0]).strip()
                attributes[attribute_name] = attribute_value
            except IndexError:
                continue
        return attributes

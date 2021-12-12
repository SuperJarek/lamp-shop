import json


class ShoppingItem:

    def __init__(self):
        self.id = ""
        self.name = ""
        self.price_pln = ""
        self.description = ""
        
        self.main_photo_uri = ""
        self.photos = []

        self.categories = []
        self.attributes = {}

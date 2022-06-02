
from django.conf import settings

from product.models import Product

class Favorites(object):
    def __init__(self,req) -> None:
        self.session = req.session
        favorites = self.session.get(settings.FAVORITES_SESSION_ID)

        if not favorites:
            favorites = self.session[settings.FAVORITES_SESSION_ID] = {}

        self.favorites = favorites
        
        settings.KEYS = self.favorites.keys()
             
    
    def __iter__(self):
        for p in self.favorites.keys():
            self.favorites[str(p)]['is-favorites'] = True

    def __len__(self):
        return sum( item for item in self.favorites.values() )
    
    def add(self,product_id):
        product_id = str(product_id)

        if product_id  not in self.favorites:
            self.favorites[product_id]= { 'product': product_id,'is_favorites':True }

        self.save()

    def remove(self,product_id):
        product_id = str(product_id)
        if product_id in self.favorites :
            del self.favorites[product_id]
            self.save()

    def save(self):
        self.session[settings.FAVORITES_SESSION_ID] = self.favorites
        self.session.modified = True

    
    def clear(self):
        del self.session[settings.FAVORITES_SESSION_ID]
        self.session.modified = True

        

    
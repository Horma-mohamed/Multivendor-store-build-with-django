from  .cart import Cart
from .favorites import Favorites

def cart(req):
    return {'cart':Cart(req).cart}

def favourites(req):
    return {'favorites':Favorites(req).favorites}



from .models import Category

def menu_categories(req):
    categories = Category.objects.all()
    return {'menu_categories':categories}
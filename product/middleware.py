from .models import Product


class ProductIsActiveMiddleware:

    def __init__(self,get_response) :
        self.get_response = get_response
        self.name= ' Abdeli '
    def __call__(self, request):
        response = self.get_response(request)
        #print('it works!!')
        return response
    
    # def process_template_response(self,request,response):
    #     response.context_data['new_data'] = self.name
    #     print(response.context_data['new_data'],self.name)
    #     return response
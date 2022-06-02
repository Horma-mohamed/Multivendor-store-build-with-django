from .models import Order
def data_statistic(req):
    orders =Order.objects.all()
    dataset = {
        'orders_chart':[
            {'jan':orders.filter(created_at__month='1')},
            {'apr':orders.filter(created_at__month='2')},
            {'feb':orders.filter(created_at__month='3')},
            {'mar':orders.filter(created_at__month='4')},
            {'may':orders.filter(created_at__month='5')},
            {'jun':orders.filter(created_at__month='6')},
            {'jul':orders.filter(created_at__month='7')},
        ]
    }
    return {'statistic_data':dataset['orders_chart']}
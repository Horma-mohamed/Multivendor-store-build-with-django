from datetime import datetime, timedelta
from notifications.models import Notification

def notifcations(req):
    if req.user.is_authenticated:
        today_date = datetime.today().strftime("%Y-%m-%d")
        yesterday_date = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        today_notifications = Notification.objects.filter(recipient=req.user,timestamp__date=today_date)
        yesterday_notification = Notification.objects.filter(recipient=req.user,timestamp__date=yesterday_date)
        return {'today_notifications':today_notifications,'yesterday_notification':yesterday_notification}
    else : 
        return []
    
from django.urls import path
from .views import TicketCreateView


app_name = 'feed'

urlpatterns = [
    path('add_ticket/', TicketCreateView.as_view(), name='add_ticket'),
]
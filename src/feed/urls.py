from django.urls import path
from .views import TicketCreateView, TicketListView, TicketUpdateView, TicketDeleteView


app_name = 'feed'

urlpatterns = [
    path('add_ticket/', TicketCreateView.as_view(), name='add_ticket'),
    path('my_tickets/', TicketListView.as_view(), name='ticket_list'),
    path('edit_ticket/<int:pk>/', TicketUpdateView.as_view(), name='edit_ticket'),
    path('delete_ticket/<int:pk>/', TicketDeleteView.as_view(), name='delete_ticket'),

]
from django.urls import path
from .views import (TicketCreateView, TicketListView, TicketUpdateView, 
                    TicketDeleteView, ReviewCreateView, ReviewUpdateView,
                    ReviewDeleteView, UserFollowsCreateView, unfollowView)


app_name = 'feed'

urlpatterns = [
    path('add_ticket/', TicketCreateView.as_view(), name='add_ticket'),
    path('my_tickets/', TicketListView.as_view(), name='ticket_list'),
    path('edit_ticket/<int:pk>/', TicketUpdateView.as_view(), name='edit_ticket'),
    path('delete_ticket/<int:pk>/', TicketDeleteView.as_view(), name='delete_ticket'),
    path('add_review/<int:pk>/', ReviewCreateView.as_view(), name='add_review'),
    path('edit_review/<int:pk>/', ReviewUpdateView.as_view(), name='edit_review'),
    path('delete_review/<int:pk>/', ReviewDeleteView.as_view(), name='delete_review'),
    path('follows/', UserFollowsCreateView.as_view(), name='follow_list'),
    path('unfollow/<int:pk>/', unfollowView.as_view(), name='unfollow'),

]
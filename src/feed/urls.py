from django.urls import path
from .views import (TicketCreateView, TicketListView, TicketUpdateView, 
                    TicketDeleteView, ReviewCreateView, ReviewUpdateView,
                    ReviewDeleteView, UserFollowsCreateView, unfollowView, 
                    add_follow, FeedView, TicketDetailView, CreateTicketAndReviewView)


app_name = 'feed'

urlpatterns = [
    path('add_ticket_and_review/', CreateTicketAndReviewView.as_view(), name='add_ticket_and_review'),
    path('feed/', FeedView.as_view(), name='feed'),
    path('ticket/<int:pk>/', TicketDetailView.as_view(), name='ticket_detail'),
    path('add_follow/', add_follow, name='add_follow'),
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
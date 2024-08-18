from django.db.models.query import QuerySet
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse, reverse_lazy
from .models import Ticket, Review
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class ReviewCreateView(LoginRequiredMixin, CreateView):
    """View for creating a review."""
    model = Review
    fields = ['ticket','rating', 'headline', 'body']
    template_name = 'feed/review_create.html'

    def form_valid(self, form):
        """Set the user of the review to the current user."""
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        """Return the URL to redirect to after creating a review."""
        return reverse('feed:ticket_list', kwargs={'pk': self.object.ticket.pk})


class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View for updating a review"""
    model = Review
    fields = ['rating', 'headline', 'body']
    template_name = 'feed/review_update_form.html'

    def get_queryset(self):
        """Return the reviews of the current user."""
        return Review.objects.filter(user=self.request.user)

    def get_success_url(self):
        """Return the URL to redirect to after updating a review."""
        return reverse('feed:ticket_list', kwargs={'pk': self.object.ticket.pk})


class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """View for deleting a review."""
    model = Review  
    template_name = 'feed/review_confirm_delete.html'

    def get_queryset(self):
        """Return the reviews of the current user."""
        return Review.objects.filter(user=self.request.user)

    def get_success_url(self):
        """Return the URL to redirect to after deleting a review."""
        return reverse('feed:ticket_list', kwargs={'pk': self.object.ticket.pk})


class TicketCreateView(LoginRequiredMixin, CreateView):
    """View for creating a ticket."""
    model = Ticket
    fields = ['title', 'description', 'image']
    template_name = 'feed/ticket_create.html'
    success_url = reverse_lazy('feed:ticket_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    

class TicketUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View for updating a ticket."""
    model = Ticket
    fields = ['title', 'description', 'image']
    template_name = 'feed/ticket_update_form.html'
    success_url = reverse_lazy('feed:ticket_list')

    def test_func(self):
        ticket = self.get_object()
        return ticket.user == self.request.user
    

class TicketDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """View for deleting a ticket."""
    model = Ticket
    template_name = 'feed/ticket_confirm_delete.html'
    success_url = reverse_lazy('feed:ticket_list')

    def test_func(self):
        ticket = self.get_object()
        return ticket.user == self.request.user
    

class TicketListView(LoginRequiredMixin, ListView):
    """View for listing tickets."""
    model = Ticket
    template_name = 'feed/ticket_list.html'
    context_object_name = 'tickets'
    ordering = ['-time_created']
    
    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user)
    


    





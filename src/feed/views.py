from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Ticket
from django.contrib.auth.mixins import LoginRequiredMixin

class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    fields = ['title', 'description', 'image']
    template_name = 'feed/ticket_create.html'
    success_url = reverse_lazy('feed:ticket_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)



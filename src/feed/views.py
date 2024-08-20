from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse, reverse_lazy
from .models import Ticket, Review, UserFollows
from .forms import UserFollowForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages

User = get_user_model()


# class FollowersListView(LoginRequiredMixin, ListView):
#     """View for listing followers of the current user."""
#     model = UserFollows
#     template_name = 'feed/followers_list.html'
#     context_object_name = 'followers'

#     def get_queryset(self):
#         """Return the followers of the current user."""
#         return UserFollows.objects.filter(followed_user=self.request.user)
    

@login_required
def add_follow(request):
    """add a follow."""
    if request.method == 'POST':
        form = UserFollowForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            try:
                followed_user = User.objects.get(username=username)
                if UserFollows.objects.filter(user=request.user, followed_user=followed_user).exists():
                    form.add_error(None, 'Vous suivez déjà cet utilisateur.')
                else:
                    UserFollows.objects.create(user=request.user, followed_user=followed_user)
                    return redirect('feed:follow_list')
            except User.DoesNotExist:
                form.add_error('username', 'Cet utilisateur n\'existe pas.')
    else:
        form = UserFollowForm()
    return render(request, 'feed/add_follow.html', {'form': form})


class UserFollowsCreateView(LoginRequiredMixin, ListView):
    """View for following a user."""
    model = UserFollows
    template_name = 'feed/user_follows.html'
    context_object_name = 'follows'

    def get_queryset(self):
        return UserFollows.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UserFollowForm()
        context['followers'] = UserFollows.objects.filter(followed_user=self.request.user)
        return context
    
    def post(self, request, *args, **kwargs):
        form = UserFollowForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            try:
                followed_user = User.objects.get(username=username)
                if UserFollows.objects.filter(user=request.user, followed_user=followed_user).exists():
                    messages.error(request, 'Vous suivez déjà cet utilisateur.')
                else:
                    UserFollows.objects.create(user=request.user, followed_user=followed_user)
                    messages.success(request, 'Utilisateur suivi avec succès.')
                    return redirect('feed:follow_list')
            except User.DoesNotExist:
                messages.error(request, 'Cet utilisateur n\'existe pas.')
        else:
            # Gestion des erreurs du formulaire
            for error in form.errors.values():
                messages.error(request, error.as_text())
        return super().get(request, *args, **kwargs)  # Rediriger vers la même page avec les messages d'erreur.

 

class unfollowView(LoginRequiredMixin, DeleteView):
    model = UserFollows
    success_url = reverse_lazy('feed:follow_list')

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class ReviewCreateView(LoginRequiredMixin, CreateView):
    """View for creating a review."""
    model = Review
    fields = ['ticket','rating', 'headline', 'body']
    template_name = 'feed/review_create_form.html'

    def form_valid(self, form):
        """Set the user of the review to the current user."""
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        """Return the URL to redirect to after creating a review."""
        return reverse('feed:ticket_list')


class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View for updating a review"""
    model = Review
    fields = ['rating', 'headline', 'body']
    template_name = 'feed/review_update_form.html'

    def test_func(self):
        # Récupère l'objet review en cours de modification
        review = self.get_object()
        # Vérifie que l'utilisateur actuel est l'auteur de la critique
        return self.request.user == review.user

    def get_queryset(self):
        """Return the reviews of the current user."""
        return Review.objects.filter(user=self.request.user)

    def get_success_url(self):
        """Return the URL to redirect to after updating a review."""
        return reverse('feed:ticket_list')


class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """View for deleting a review."""
    model = Review  
    template_name = 'feed/review_confirm_delete.html'

    def test_func(self):
        # Récupère l'objet review en cours de modification
        review = self.get_object()
        # Vérifie que l'utilisateur actuel est l'auteur de la critique
        return self.request.user == review.user

    def get_queryset(self):
        """Return the reviews of the current user."""
        return Review.objects.filter(user=self.request.user)

    def get_success_url(self):
        """Return the URL to redirect to after deleting a review."""
        return reverse('feed:ticket_list')


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
    


    





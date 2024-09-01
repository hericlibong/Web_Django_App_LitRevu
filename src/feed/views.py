from django.db.models import Q, Prefetch, Count, Value, CharField, F
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse, reverse_lazy
from .models import Ticket, Review, UserFollows
from .forms import UserFollowForm, ReviewForm, TicketForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from itertools import chain


User = get_user_model()


class CreateTicketAndReviewView(LoginRequiredMixin, CreateView):
    """View for creating a ticket and a review."""
    model = Ticket
    form_class = TicketForm
    template_name = 'feed/create_ticket_and_review.html'

    def form_valid(self, form):
        # Assigner l'utilisateur avant de sauvegarder le formulaire du billet
        form.instance.user = self.request.user
        response = super().form_valid(form)
        # Traiter le formulaire de critique si le billet est validement créé
        review_form = ReviewForm(self.request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.ticket = self.object  # Le nouveau billet créé
            review.user = self.request.user
            review.save()
        return response

    def get_success_url(self):
        """Return the URL to redirect to after creating a ticket and a review."""
        return reverse('feed:feed')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'review_form' not in context:
            context['review_form'] = ReviewForm(self.request.POST or None)
        return context


class TicketDetailView(LoginRequiredMixin, DetailView):
    """View for see a single ticket with all the reviews."""
    model = Ticket
    template_name = 'feed/ticket_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = self.object.review_set.all().order_by('-time_created')
        context['stars'] = range(1, 6)
        return context


class FeedView(LoginRequiredMixin, ListView):
    """View for the feed."""
    template_name = 'feed/feed.html'
    context_object_name = 'feed_items'
    paginate_by = 5

    def get_queryset(self):
        user = self.request.user
        followed_users = UserFollows.objects.filter(user=user).values_list('followed_user', flat=True)
        recent_reviews_prefetch = Prefetch(
            'review_set',
            queryset=Review.objects.order_by('-time_created')[:2],
            to_attr='recent_reviews'
        )
        tickets = Ticket.objects.filter(
            Q(user__in=followed_users) | Q(user=user)
        ).prefetch_related(recent_reviews_prefetch).annotate(num_reviews=Count('review')).order_by('-time_created')
        return tickets

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stars'] = range(1, 6)
        return context


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
    form_class = ReviewForm
    template_name = 'feed/review_create_form.html'

    def form_valid(self, form):
        # Vérification pour éviter la duplication de critique pour le même ticket par le même utilisateur
        self.ticket = get_object_or_404(Ticket, pk=self.kwargs.get('pk'))
        existing_review = Review.objects.filter(ticket=self.ticket, user=self.request.user).exists()
        if existing_review:
            form.add_error(None, 'Vous avez déjà publié une critique pour ce billet.')
            form.add_error(None, 'Cliquez pour retourner au flux.')
            return self.form_invalid(form)

        form.instance.user = self.request.user
        form.instance.ticket = self.ticket
        return super().form_valid(form)

    def get_success_url(self):
        """Return the URL to redirect to after creating a review."""
        return reverse('feed:feed')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ticket'] = get_object_or_404(Ticket, pk=self.kwargs.get('pk'))
        return context


class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View for updating a review"""
    model = Review
    form_class = ReviewForm
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
        return reverse('feed:posts')


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
        return reverse('feed:posts')


class TicketCreateView(LoginRequiredMixin, CreateView):
    """View for creating a ticket."""
    model = Ticket
    form_class = TicketForm
    template_name = 'feed/ticket_create.html'
    success_url = reverse_lazy('feed:feed')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TicketUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View for updating a ticket."""
    model = Ticket
    form_class = TicketForm
    template_name = 'feed/ticket_update_form.html'
    success_url = reverse_lazy('feed:posts')

    def test_func(self):
        ticket = self.get_object()
        return ticket.user == self.request.user


class TicketDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """View for deleting a ticket."""
    model = Ticket
    template_name = 'feed/ticket_confirm_delete.html'
    success_url = reverse_lazy('feed:posts')

    def test_func(self):
        ticket = self.get_object()
        return ticket.user == self.request.user


class PostsListView(LoginRequiredMixin, ListView):
    """View for listing tickets and reviews."""
    template_name = 'feed/posts_list.html'
    context_object_name = 'items'
    paginate_by = 5

    def get_queryset(self):
        user = self.request.user
        # Récupérer les tickets de l'utilisateur
        tickets = Ticket.objects.filter(user=user).prefetch_related('review_set').annotate(
            content_type=Value('ticket', output_field=CharField()),
            sort_date=F('time_created')
        )

        # Récupérer les critiques de l'utilisateur sur les tickets d'autres utilisateurs
        reviews = Review.objects.filter(user=user).exclude(ticket__user=user).select_related('ticket').annotate(
            content_type=Value('review', output_field=CharField()),
            sort_date=F('time_created')
        )

        # Combiner les deux querysets et les trier par date de création
        result_list = sorted(
            chain(tickets, reviews),
            key=lambda instance: instance.sort_date,
            reverse=True
        )
        return result_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stars'] = range(1, 6)
        return context

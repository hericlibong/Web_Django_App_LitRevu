from django.contrib import admin
from .models import Ticket, Review, UserFollows


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'time_created')
    search_fields = ('title', 'user__username')
    list_filter = ('time_created',)
    readonly_fields = ('time_created',)

    fieldsets = (
        ('first informations', {
            'fields': ('title', 'description', 'user',)
        }),
        ('Date information', {
            'fields': ('time_created',)
        }),
        ('Image', {
            'fields': ('image',)
        }),
    )

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'rating', 'headline', 'user', 'time_created')
    search_fields = ('ticket__title', 'headline', 'user__username')
    list_filter = ('time_created', 'rating')
    readonly_fields = ('time_created',)

    fieldsets = (
        ('first informations', {
            'fields': ('ticket', 'rating', 'headline', 'body', 'user',)
        }),
        ('Date information', {
            'fields': ('time_created',)
        }),
    )

@admin.register(UserFollows)
class UserFollowsAdmin(admin.ModelAdmin):
    list_display = ('user', 'followed_user')
    search_fields = ('user__username', 'followed_user__username')



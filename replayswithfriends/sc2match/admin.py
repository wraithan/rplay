from django.contrib import admin
from .models import Match, PlayerResult, Map, Player


class PlayerResultInline(admin.StackedInline):
    model = PlayerResult


class PlayerInline(admin.StackedInline):
    model = Player


class MatchAdmin(admin.ModelAdmin):
    list_display = ['id', '__unicode__']
    readonly_fields = [
        'mapfield',
        'duration',
    ]
    inlines = [PlayerResultInline]


class PlayerResultAdmin(admin.ModelAdmin):
    list_display = ['player', 'match']
    inlines = [PlayerInline]


class PlayerAdmin(admin.ModelAdmin):
    pass



admin.site.register(PlayerResult, PlayerResultAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(Map)
admin.site.register(Player, PlayerAdmin)

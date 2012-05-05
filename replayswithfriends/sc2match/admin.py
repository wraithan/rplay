from django.contrib import admin
from .models import Match, PlayerResult, Map, Player
from .tasks import parse_replay

class PlayerResultInline(admin.StackedInline):
    model = PlayerResult


class PlayerInline(admin.StackedInline):
    model = Player

class MatchAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'owner',
        '__unicode__',
        'processed',
        'process_error',
    ]
    readonly_fields = [
        'mapfield',
        'duration',
    ]
    inlines = [PlayerResultInline]

    def process_match(self, request, queryset):
        for match in queryset:
            parse_replay.delay(match.id)
    #process_match.short_description("Reprocess Matches")

    actions = [process_match]


class PlayerResultAdmin(admin.ModelAdmin):
    list_display = ['player', 'match']
    inlines = [PlayerInline]


class PlayerAdmin(admin.ModelAdmin):
    pass



admin.site.register(PlayerResult, PlayerResultAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(Map)
admin.site.register(Player, PlayerAdmin)

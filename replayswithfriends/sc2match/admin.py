from django.contrib import admin
from .models import Match, PlayerResult, Map, Player, MatchMessage
from .tasks import parse_replay


class MessageInline(admin.TabularInline):
    model = MatchMessage
    extra = 0

class PlayerResultInline(admin.StackedInline):
    model = PlayerResult
    extra = 0

class PlayerInline(admin.StackedInline):
    model = Player

class MatchAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'owner',
        '__unicode__',
        'game_played_on',
        'processed',
        'process_error',
        'matchhash',
    ]
    readonly_fields = [
        'mapfield',
        'duration',
        'matchhash',
        'process_error',
    ]
    inlines = [PlayerResultInline, MessageInline]

    def process_match(self, request, queryset):
        for match in queryset:
            match.process_now()

    def deferred_process_match(self, request, queryset):
        for match in queryset:
            parse_replay.delay(match.id)
    #process_match.short_description("Reprocess Matches")

    actions = [process_match, deferred_process_match]


class PlayerResultAdmin(admin.ModelAdmin):
    list_display = ['player', 'match']
    inlines = [PlayerInline]


class PlayerAdmin(admin.ModelAdmin):
    pass

class MapAdmin(admin.ModelAdmin):
    readonly_fields = [
        'url',
    ]


admin.site.register(PlayerResult, PlayerResultAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(Map, MapAdmin)
admin.site.register(Player, PlayerAdmin)

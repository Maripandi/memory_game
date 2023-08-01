from django.contrib import admin
from game.models import Card,Score,Game
# Register your models here.
admin.site.register(Card)
admin.site.register(Game)
admin.site.register(Score)
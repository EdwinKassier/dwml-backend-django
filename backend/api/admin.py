from django.contrib import admin

# Register your models here.
from api.models.portfolio import Results, LOGGING
from api.models.market_data import OpeningAverage

admin.site.register(Results)
admin.site.register(OpeningAverage)
admin.site.register(LOGGING)

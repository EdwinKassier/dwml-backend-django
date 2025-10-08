from api.models.market_data import OpeningAverage

# Register your models here.
from api.models.portfolio import PortfolioLog, PortfolioResult
from django.contrib import admin

admin.site.register(PortfolioResult)
admin.site.register(OpeningAverage)
admin.site.register(PortfolioLog)

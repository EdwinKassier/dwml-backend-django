from django.contrib import admin

# Register your models here.
from api.models.portfolio import PortfolioResult, PortfolioLog
from api.models.market_data import OpeningAverage

admin.site.register(PortfolioResult)
admin.site.register(OpeningAverage)
admin.site.register(PortfolioLog)

from django.contrib import admin

# Register your models here.
from api.models import Results,OPENING_AVERAGE,LOGGING

admin.site.register(Results)
admin.site.register(OPENING_AVERAGE)
admin.site.register(LOGGING)


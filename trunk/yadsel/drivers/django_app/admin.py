# Admin registrations
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

from yadsel.drivers.django_app.models import YadselHistory, YadselLog

class YadselHistoryAdmin(ModelAdmin):
    list_display = ['version_space', 'version_number', 'change_date', 'errors']

class YadselLogAdmin(ModelAdmin):
    search_fields = ['msg','version_space','version_number',]
    list_display = ['version_space', 'version_number', 'log_date']

admin.site.register(YadselHistory, YadselHistoryAdmin)
admin.site.register(YadselLog, YadselLogAdmin)



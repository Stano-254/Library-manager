from django.contrib import admin

from base.models import State


# Register your models here.
@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    """
    state admin site
    """
    list_display = ('name', 'description', 'date_modified', 'date_created')
    search_fields = ('name',)

from django.contrib import admin

from base.models import State, Transaction, TransactionType, UserIdentity


# Register your models here.
@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    """
    state admin site
    """
    list_display = ('name', 'description', 'date_modified', 'date_created')
    search_fields = ('name',)


@admin.register(TransactionType)
class TransactionTypeAdmin(admin.ModelAdmin):
    """
    TransactionType admin site
    """
    list_display = ('name', 'description', 'simple_name', 'state', 'date_modified', 'date_created')
    search_fields = ('name',)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """
    Transaction admin site
    """
    list_display = (
    'transaction_type', 'request', 'message', 'response_code', 'response', 'state', 'date_modified', 'date_created')
    search_fields = ('transaction_type',)
    list_filter = ('transaction_type', 'state')


@admin.register(UserIdentity)
class UserIdentityAdmin(admin.ModelAdmin):
    """
    Transaction admin site
    """
    list_display = (
    'token', 'user', 'source_ip', 'state')
    search_fields = ('token',)
    list_filter = ('source_ip', 'state')

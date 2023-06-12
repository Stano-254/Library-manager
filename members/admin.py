from django.contrib import admin

from members.models import Members


# Register your models here.
@admin.register(Members)
class MemberAdmin(admin.ModelAdmin):
    """
    member admin site
    """
    list_display = ('first_name', 'last_name', 'national_id', 'mobile_no', 'gender',
                    'membership_no', 'state', 'date_modified', 'date_created')
    search_fields = ('national_id', 'membership_no')
    list_filter = ('state__name', 'date_created')

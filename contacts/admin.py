from django.contrib import admin
from .models import Contact

class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email',
                    'phone', 'contact_date', 'user_id')
    list_display_links = ('id', 'name')
    list_filter = ('user_id', 'listing')
    search_fields = ('name', 'email', 'listing')
    list_per_page = 10

admin.site.register(Contact, ContactAdmin)

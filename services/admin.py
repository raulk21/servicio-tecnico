from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Service, ContactRequest

# Register your models here.

@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'service', 'colored_status', 'created_at')
    list_filter = ('status', 'service')
    search_fields = ('name', 'email')

    def colored_status(self, obj):
        if obj.status == 'pendiente':
            color = 'orange'
        elif obj.status == 'proceso':
            color = 'blue'
        elif obj.status == 'finalizado':
            color = 'green'
        else:
            color = 'black'

        return format_html(
            '<strong style="color: {};">{}</strong>',
            color,
            obj.get_status_display()
        )

    colored_status.short_description = 'Estado'
    
admin.site.register(Category)
admin.site.register(Service)

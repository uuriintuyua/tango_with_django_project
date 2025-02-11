from django.contrib import admin
from rango.models import Category, Page

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')  # This will display the category, title, and URL

admin.site.register(Category)

admin.site.register(Page, PageAdmin)
# Register your models here.

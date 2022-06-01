from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from.models import Menu


@admin.register(Menu)
class MenuAdmin(SortableAdminMixin, TranslationAdmin):
    list_display = ['title', 'item_url', 'target', 'position', 'show_item', ]
    list_filter = ['position', 'show_item', 'target', 'position']

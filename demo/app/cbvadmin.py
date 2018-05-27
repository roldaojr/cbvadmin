from __future__ import unicode_literals, absolute_import
import cbvadmin
from menu import MenuItem
from .models import Category, Computer


@cbvadmin.register(Category)
class CategoryAdmin(cbvadmin.ModelAdmin):
    list_display = ('name',)


@cbvadmin.register(Computer)
class ComputerAdmin(cbvadmin.ModelAdmin):
    list_display = ('name', 'category', 'active')
    filter_fields = ('name', 'active')

    def get_menu(self):
        menu = super(ComputerAdmin, self).get_menu()
        return menu + [MenuItem(
            'Invisible menu', '', submenu=False, children=[
                MenuItem('Invisible Item', '', check=lambda r: False)
            ])]

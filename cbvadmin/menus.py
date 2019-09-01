from menu import Menu
from .sites import site

for item in site.get_menu():
    Menu.add_item('cbvadmin', item)

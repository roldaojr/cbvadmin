# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from menu import Menu
from .sites import site

for item in site.get_menu():
    Menu.add_item('cbvadmin', item)

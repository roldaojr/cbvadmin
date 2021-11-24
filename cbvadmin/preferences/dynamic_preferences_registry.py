from django.utils.translation import gettext_lazy as _
from dynamic_preferences.types import (
    BooleanPreference, ChoicePreference
)
from dynamic_preferences.preferences import Section
from .registries import site_preferences_registry
from ..widgets import ThemeColorWidget, SwitchInput

appearance = Section('appearance', 'Appearance')

color_choices = (
    ('red', _('Red')),
    ('pink', _('Pink')),
    ('fuchsia', _('Fuchsia')),
    ('orange', _('Orange')),
    ('warning', _('Yeloow')),
    ('purple', _('Purple')),
    ('indigo', _('Indigo')),
    ('blue', _('Blue')),
    ('navy', _('Navy')),
    ('lightblue', _('Light Blue')),
    ('info', _('Cyan')),
    ('olive', _('Olive')),
    ('green', _('Verde')),
    ('teal', _('Teal')),
    ('lime', _('Lime')),
)


@site_preferences_registry.register
class DarkMode(BooleanPreference):
    section = appearance
    name = 'dark_mode'
    verbose_name = _('Dark mode')
    widget = SwitchInput
    default = False


@site_preferences_registry.register
class NavbarColor(ChoicePreference):
    section = appearance
    name = 'navbar_color'
    verbose_name = _('Navigation bar color')
    widget = ThemeColorWidget
    default = 'white'
    choices = (
        ('red', _('Red')),
        ('pink', _('Pink')),
        ('fuchsia', _('Fuchsia')),
        ('orange', _('Orange')),
        ('yellow', _('Yellow')),
        ('purple', _('Purple')),
        ('indigo', _('Indigo')),
        ('blue', _('Blue')),
        ('navy', _('Navy')),
        ('lightblue', _('Light Blue')),
        ('cyan', _('Cyan')),
        ('olive', _('Olive')),
        ('green', _('Green')),
        ('teal', _('Teal')),
        ('lime', _('Limee')),
        ('white', _('White')),
        ('light', _('Gray light')),
        ('gray', _('Gray')),
        ('gray-dark', _('Gray dark')),
        ('black', _('Black')),
    )


@site_preferences_registry.register
class AccentColor(ChoicePreference):
    section = appearance
    name = 'accent_color'
    verbose_name = _('Accent color')
    widget = ThemeColorWidget
    default = ''
    choices = [
        ('', _('None'))
    ] + list(color_choices)


@site_preferences_registry.register
class SidebarColor(ChoicePreference):
    section = appearance
    name = 'sidebar_color'
    verbose_name = _('Sidebar color')
    widget = ThemeColorWidget
    default = 'blue'
    choices = color_choices


@site_preferences_registry.register
class SidebarDark(BooleanPreference):
    section = appearance
    name = 'dark_sidebar'
    verbose_name = _('Dark sidebar')
    widget = SwitchInput
    default = True


@site_preferences_registry.register
class SidebarFlat(BooleanPreference):
    section = appearance
    name = 'sidebar_flat'
    verbose_name = _('Flat sidebar')
    widget = SwitchInput
    default = False


@site_preferences_registry.register
class SidebarCompact(BooleanPreference):
    section = appearance
    name = 'sidebar_compact'
    verbose_name = _('Compact sidebar')
    widget = SwitchInput
    default = False

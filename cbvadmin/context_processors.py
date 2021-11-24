from django.conf import settings
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch

light_colors = 'light', 'white', 'warning', 'lime'


def features(request):
    available = {}
    if 'django.contrib.sites' in settings.INSTALLED_APPS:
        available['enable_sites'] = True
    try:
        reverse('cbvadmin:preferences:global')
        available['enable_global_preferences'] = True
    except NoReverseMatch:
        available['enable_global_preferences'] = False
    try:
        reverse('cbvadmin:preferences:user')
        available['enable_user_preferences'] = True
    except NoReverseMatch:
        available['enable_user_preferences'] = False
    try:
        reverse('cbvadmin:preferences:site')
        available['enable_site_preferences'] = True
    except NoReverseMatch:
        available['enable_site_preferences'] = False
    return available


def appearance(request):
    if not hasattr(request, 'site') or not hasattr(request.site, 'preferences'):
        return None
    prefix = 'appearance'
    appearance = {
        key[len(prefix) + 2:]: value
        for key, value in request.site.preferences.items()
        if key.startswith(prefix)
    }
    navbar_color = appearance.get('navbar_color', None)
    if navbar_color:
        if navbar_color in light_colors:
            appearance['navbar_tone'] = 'light'
        else:
            appearance['navbar_tone'] = 'dark'
    if appearance.get('dark_sidebar', True):
        appearance['sidebar_tone'] = 'dark'
    else:
        appearance['sidebar_tone'] = 'light'
    return appearance


def site(request):
    return {
        'cbvadmin': features(request),
        'appearance': appearance(request)
    }

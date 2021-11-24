from django.forms import BooleanField


class BooleanSwitchField(BooleanField):
    css_classes = 'custom-switch'

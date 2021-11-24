from django.forms.widgets import RadioSelect, CheckboxInput


class ThemeColorWidget(RadioSelect):
    button_group = True


class SwitchInput(CheckboxInput):
    is_switch = True

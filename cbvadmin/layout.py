from django.template.loader import render_to_string
from crispy_forms.helper import FormHelper
from crispy_forms.utils import flatatt
from crispy_forms.layout import *
from .fields import valuefield_for_formfield, ValueField


class Row(Div):
    css_class = 'row'


class Column(Div):
    css_class = 'col'


class Button(Button):
    """
    Used to create a Submit input descriptor for the {% crispy %} template tag:
    .. sourcecode:: python
        button = Button('Button 1', 'Press Me!')
    .. note:: The first argument is also slugified and turned into the
    id for the button.
    """
    input_type = 'button'
    field_classes = 'btn waves-effect waves-light'


class Submit(Submit):
    """
    Used to create a Submit button descriptor for the {% crispy %}
    template tag:
    .. sourcecode:: python
        submit = Submit('Search the Site', 'search this site')
    .. note:: The first argument is also slugified and turned into the id for
              the submit button.
    """
    input_type = 'submit'
    field_classes = 'btn waves-effect waves-light'


class StrictField(Field):
    template = "%s/field.strict.html"


class StaticField(Field):
    template = "%s/field.static.html"

    def __init__(self, *args, format=None, **kwargs):
        self.format = format
        super().__init__(*args, **kwargs)

    def render_static_field(self, field, form, form_style, context, **kwargs):
        template = self.get_template_name(kwargs.get('template_pack'))
        attrs = self.attrs

        if form and field in form.fields:
            value = form[field].value
        else:
            value = getattr(form.instance, field, None)

        text = getattr(form.instance, field, None)
        if callable(self.format):
            text = self.format(text)

        field = {
            'auto_id': field,
            'name': field,
            'value': value,
            'text': text,
            'form': form
        }

        context.update({
            'wrapper_class': self.wrapper_class,
            'field': field,
            'flat_attrs': flatatt(attrs if isinstance(attrs, dict) else {}),
        })

        if kwargs.get('extra_context') is not None:
            context.update(kwargs.get('extra_context'))

        return render_to_string(template, context.flatten())

    def render(self, *args, **kwargs):
        return ''.join(
            self.render_static_field(field, *args, **kwargs)
            for field in self.fields
        )

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


def instance_getter(self):
    return getattr(self.form.instance, self.name, None)


class StaticField(Field):
    template = "%s/field.static.html"

    def __init__(self, *args, **kwargs):
        self._filter_func = kwargs.pop('filter_func', None)
        super(StaticField, self).__init__(*args, **kwargs)

    def _lookup_field(self, field_name, form):
        try:
            return valuefield_for_formfield(
                form[field_name], filter_func=self._filter_func)
        except KeyError:
            return ValueField(form.instance, field_name,
                              filter_func=self._filter_func)

    def render_field(self, field, context, template):
        attrs = self.attrs
        context.update({
            'wrapper_class': self.wrapper_class,
            'field': field,
            'flat_attrs': flatatt(attrs if isinstance(attrs, dict) else {}),
        })
        return render_to_string(template, context)

    def render(self, form, form_style, context, *args, **kwargs):
        fields = [self._lookup_field(field, form) for field in self.fields]
        template = self.get_template_name(kwargs.get('template_pack'))
        context.update(kwargs.get('extra_context', {}))
        return ''.join(self.render_field(field, context, template)
                       for field in fields)

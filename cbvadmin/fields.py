# pylint: disable=protected-access
from django.core.exceptions import ObjectDoesNotExist, FieldDoesNotExist


def is_rel_field(name, model):
    if hasattr(name, 'split') and name.find("__") > 0:
        parts = name.split("__")
        if parts[0] in model._meta.get_all_field_names():
            return True
    return False


def lookup_field(name, obj, model_admin=None):
    opts = obj._meta
    try:
        f = opts.get_field(name)
    except FieldDoesNotExist:
        # For non-field values, the value is either a method, property or
        # returned via a callable.
        if callable(name):
            attr = name
            value = attr(obj)
        elif (model_admin is not None and hasattr(model_admin, name) and
              name not in ('__str__', '__unicode__')):
            attr = getattr(model_admin, name)
            value = attr(obj)
        else:
            if is_rel_field(name, obj):
                parts = name.split("__")
                rel_name, sub_rel_name = parts[0], "__".join(parts[1:])
                rel_obj = getattr(obj, rel_name)
                if rel_obj is not None:
                    return lookup_field(sub_rel_name, rel_obj, model_admin)
            attr = getattr(obj, name)
            if callable(attr):
                value = attr()
            else:
                value = attr
        f = None
    else:
        attr = None
        value = getattr(obj, name)
    return f, attr, value


class ValueField():
    def __init__(self, obj, field_name, filter_func=None):
        try:
            f, attr, value = lookup_field(field_name, obj)
        except (AttributeError, ObjectDoesNotExist):
            pass
        self.object = obj
        self.name = field_name
        self.field = f
        if f:
            label = f.verbose_name
        elif hasattr(attr, 'verbose_name'):
            label = attr.verbose_name
        else:
            label = field_name
        self.auto_id = 'id_%s' % field_name
        self.label = label
        self.value = value

        if callable(filter_func):
            self.text = filter_func(value)
        else:
            self.text = value


def valuefield_for_formfield(field, filter_func=None):
    value_field = ValueField(field.form.instance, field.name,
                             filter_func=filter_func)
    value_field.label = field.label
    value_field.value = field.value
    value_field.form = field.form
    value_field.auto_id = 'id_%s' % field.form.add_prefix(field.name)
    return value_field

from django_tables2 import tables
from django_tables2 import columns
from django_tables2.utils import A, call_with_appropriate


class ColumnWithLink(columns.LinkColumn):
    def __init__(self, column, *args, **kwargs):
        self.instance = column
        super(ColumnWithLink, self).__init__(*args, **kwargs)

    def value(self, **kargs):
        return self.instance.value

    def render(self, *args, **kwargs):
        text = call_with_appropriate(self.instance.render, kwargs)
        return self.render_link(
            self.compose_url(kwargs['record'], kwargs['bound_column']),
            record=kwargs['record'],
            value=text
        )


def table_factory(model, fields=None, action='edit', extra={}):
    attrs = {'Meta': type('Meta', (object,), {
        'model': model, 'fields': fields})}
    if action is not None:
        link_field = fields[0] if fields else 'id'
        column = columns.library.column_for_field(
            model._meta.get_field(link_field))
        view_tuple = (model._meta.app_label, model._meta.model_name, action)
        link_column = ColumnWithLink(
            column, 'cbvadmin:%s_%s_%s' % view_tuple, args=[A('pk')])
        attrs.update({link_field: link_column})
    attrs.update(extra)
    return type('%sTable' % model._meta.object_name,
                (tables.Table,), attrs)

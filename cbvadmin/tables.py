from django_tables2 import tables
from django_tables2.utils import A


def table_factory(model, fields=None, action='edit', extra={}):
    attrs = {'Meta': type('Meta', (object,), {
        'model': model, 'fields': fields})}
    if action is not None:
        linkcol = fields[0] if fields else 'id'
        view_tuple = (model._meta.app_label, model._meta.model_name, action)
        attrs.update({linkcol: tables.columns.LinkColumn(
            'cbvadmin:%s_%s_%s' % view_tuple, args=[A('pk')])})
    attrs.update(extra)
    return type('%sTable' % model._meta.object_name,
                (tables.Table,), attrs)

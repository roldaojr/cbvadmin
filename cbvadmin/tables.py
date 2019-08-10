from django_tables2 import tables, columns


def table_factory(model, fields=None, action=None, extra={}):
    attrs = {'Meta': type('Meta', (object,), {
        'model': model, 'fields': fields})}
    if action is not None:
        link_field = fields[0] if fields else 'id'
        column = columns.library.column_for_field(
            model._meta.get_field(link_field))
        attrs.update({
            link_field: type(column)(
                linkify=(action, {"pk": tables.Accessor("pk")}))
        })

    attrs.update(extra)
    return type('%sTable' % model._meta.object_name,
                (tables.Table,), attrs)

from django.views.generic.list import ListView
from django_tables2 import SingleTableMixin, RequestConfig
from .mixins import AdminMixin, FilterMixin, PermissionRequiredMixin


class TableListMixin(PermissionRequiredMixin, AdminMixin, FilterMixin,
                     SingleTableMixin):
    template_name = 'list.html'

    def get_table_class(self):
        if not self.table_class:
            return self.admin.get_table_class()
        return self.table_class

    def get_table(self, **kwargs):
        table = super(TableListMixin, self).get_table()
        paginate = {'page': self.request.GET.get('page'),
                    'per_page': self.paginate_by}
        RequestConfig(self.request, paginate=paginate).configure(table)
        return table

    def get_table_data(self):
        if self.filterset:
            return self.filterset.qs
        else:
            return self.get_queryset()

    def get_template_names(self, *args, **kwargs):
        if 'querystring_key' in self.request.GET:
            return self.get_admin_template('table.html')
        else:
            return super(TableListMixin, self).get_template_names(
                *args, **kwargs)


class TableListView(TableListMixin, ListView):
    pass

ListView = TableListView

from django_tables2 import SingleTableView, RequestConfig
from .mixins import AdminMixin, FilterMixin, PermissionRequiredMixin


class TableListView(PermissionRequiredMixin, AdminMixin, FilterMixin,
                    SingleTableView):
    template_name = 'list.html'

    def get_table_class(self):
        if not self.table_class:
            return self.admin.get_table_class()
        return self.table_class

    def get_table(self, **kwargs):
        table = super(TableListView, self).get_table()
        paginate = {'page': self.request.GET.get('page'),
                    'per_page': self.paginate_by}
        RequestConfig(self.request, paginate=paginate).configure(table)
        return table

    def get_table_data(self):
        if self.filterset:
            return self.filterset.qs
        else:
            return self.get_queryset()


ListView = TableListView

from django.views.generic.list import ListView as BaseListView
from django_tables2 import SingleTableMixin, RequestConfig
from .mixins import AdminMixin, FilterMixin, PermissionRequiredMixin

___all__ = ('TableListMixin', 'TableListView', 'ListView')


class TableListMixin(PermissionRequiredMixin, AdminMixin, FilterMixin,
                     SingleTableMixin):
    template_name = 'list.html'

    def get_table_class(self):
        if not self.table_class:
            return self.admin.get_table_class()
        return self.table_class

    def get_table(self, **kwargs):
        table = super().get_table()
        paginate = {'page': self.request.GET.get('page'),
                    'per_page': self.paginate_by}
        RequestConfig(self.request, paginate=paginate).configure(table)
        return table

    def get_table_data(self):
        if self.filterset:
            return self.filterset.qs
        return self.get_queryset()

    def get_template_names(self, *args, **kwargs):
        if 'querystring_key' in self.request.GET:
            return self.get_admin_template('table.html')
        return super().get_template_names(*args, **kwargs)


class TableListView(TableListMixin, BaseListView):
    def get_context_data(self, **kwargs):
        if self.filterset:
            kwargs['object_list'] = self.filterset.qs
        return super().get_context_data(**kwargs)


ListView = TableListView

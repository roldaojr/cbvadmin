from django import forms
from django.contrib.auth.models import User, Group, Permission
from .layout import FormHelper, Layout, Row, Field


class UserForm(forms.ModelForm):
    user_permissions = forms.ModelMultipleChoiceField(
        Permission.objects.exclude(content_type__app_label__in=[
            'admin', 'contenttypes', 'sessions']),
        widget=forms.widgets.CheckboxSelectMultiple, required=False)
    groups = forms.ModelMultipleChoiceField(
        Group.objects.all(), widget=forms.widgets.CheckboxSelectMultiple,
        required=False)

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_id = 'change_form'
        helper.layout = Layout(
            Row(
                Field('first_name', wrapper_class='l6'),
                Field('last_name', wrapper_class='l6'),
                Field('username', wrapper_class='l6'),
                Field('email', wrapper_class='l6')),
            Row(
                Field('is_active', wrapper_class='l4'),
                Field('is_staff', wrapper_class='l4'),
                Field('is_superuser', wrapper_class='l4')),
            Row(
                Field('groups', wrapper_class='l6'),
                Field('user_permissions', wrapper_class='l6')
            ))
        return helper

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email',
                  'is_active', 'is_staff', 'is_superuser',
                  'groups', 'user_permissions')


class GroupForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        Permission.objects.exclude(content_type__app_label__in=[
            'admin', 'contenttypes', 'sessions']),
        widget=forms.widgets.CheckboxSelectMultiple, required=False)

    class Meta:
        model = Group
        fields = '__all__'

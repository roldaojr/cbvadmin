from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Computer(models.Model):
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, null=True, on_delete='set_null')

    def __str__(self):
        return self.name

from django.urls import path, reverse


class Action(object):
    view_class = None
    default = False
    item = False
    path = None
    perm = None

    def __init__(self, view_class, **kwargs):
        self.view_class = view_class
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


class BoundAction(object):
    name = None
    admin = None
    view = None
    default = False
    item = False
    path = None
    perm = None

    def __init__(self, admin, **kwargs):
        self.admin = admin
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def __str__(self):
        return '<%s>' % ' '.join([
            type(self).__name__,
            self.name,
            str(self.default),
            str(self.item)
        ])

    @property
    def url_name(self):
        return self.admin.get_url_name(self.name)

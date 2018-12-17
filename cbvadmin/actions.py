from django.urls import path, reverse


class Action(object):
    name = None
    path = None
    view = None
    perm = None
    admin = None
    view_class = None

    def __init__(self, view_class=None, **kwargs):
        self.view_class = view_class
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def as_path(self):
        if self.path is not None:
            pattern = self.path
        else:
            pattern = '%s' % self.name
        return path(pattern, self.view, name=self.name)


class ObjectAction(Action):
    def as_path(self):
        if self.path is not None:
            pattern = self.path
        else:
            pattern = '<int:pk>/%s' % self.name
        return path(pattern, self.view, name=self.name)

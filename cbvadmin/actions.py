from django.urls import path


class Action(object):
    def __init__(self, name=None, path=None, **kwargs):
        self.name = name
        self.path = path
        for key, value in kwargs.items():
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

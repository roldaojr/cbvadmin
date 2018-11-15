from django.urls import path


class Action(object):
    def __init__(self, name, path=None, *args, **kwargs):
        if not path:
            path = '%s/' % name
        self.name = name
        self.path = path
        for key, value in kwargs.items():
            setattr(self, key, value)

    def as_path(self):
        return path(self.path, self.view, name=self.name)


class ObjectAction(Action):
    def __init__(self, name, path=None):
        if not path:
            path = '<int:pk>/%s/' % name
        return super().__init__(name, path)

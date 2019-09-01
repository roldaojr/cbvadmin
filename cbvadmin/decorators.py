from .sites import site


def register(name):
    def decorated(obj):
        site.register(name, obj)
        return obj
    return decorated

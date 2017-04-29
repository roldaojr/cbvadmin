from .sites import site


def register(model_class):
    def decorated(admin_class):
        return site.register(model_class, admin_class)
    return decorated

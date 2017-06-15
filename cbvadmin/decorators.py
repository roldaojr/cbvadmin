from .sites import site


def register(model_class):
    def decorated(admin_class):
        site.register(model_class, admin_class)
        return admin_class
    return decorated

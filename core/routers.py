from .utils import get_current_db_name

class TenantRouter:
    """
    A router to control all database operations on models in the
    schools application.
    """
    tenant_apps = ['schools']
    public_apps = ['core', 'users', 'admin', 'auth', 'contenttypes', 'sessions', 'messages', 'staticfiles']

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.tenant_apps:
            return get_current_db_name()
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.tenant_apps:
            return get_current_db_name()
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        # Allow relations between tenant models and default-db models
        obj1_tenant = obj1._meta.app_label in self.tenant_apps
        obj2_tenant = obj2._meta.app_label in self.tenant_apps
        # If one is tenant and one is default, allow the relation
        if obj1_tenant != obj2_tenant:
            return True
        # If both are in the same type, allow
        return obj1_tenant == obj2_tenant

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db == 'default':
            return app_label in self.public_apps
        return True

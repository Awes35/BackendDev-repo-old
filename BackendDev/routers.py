"""
Create routers for handling routing to/from each Database

Used in settings.py DATABASE_ROUTERS list.
"""

class MasterRouter:
    
    route_app_labels = {'auth', 'contenttypes', 'admin', 'sessions'}
    
    def db_for_read(self, model, **hints):
        """
        Attempts to read auth/contenttypes/admin/sessions app models go to 'master'.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'master'
        return None
    
    def db_for_write(self, model, **hints):
        """
        Attempts to write auth/contenttypes/admin/sessions app models go to 'master'.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'master'
        return None
    
    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth/contenttypes/admin/sessions apps is involved.
        """
        if (
            obj1._meta.app_label in self.route_app_labels or
            obj2._meta.app_label in self.route_app_labels
        ):
           return True
        return None
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth/contenttypes/admin/sessions apps only appear in the 'master' database.
        """
        if app_label in self.route_app_labels:
            return db == 'master'
        return None


class ContentRouter:
    
    route_app_labels = {'data'}

    def db_for_read(self, model, **hints):
        """
        Data app reads goes to 'content' db.
        """
        return 'content'
    
    def db_for_write(self, model, **hints):
        """
        Data app writes always go to 'content' db.
        """
        return 'content'
    
    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the data app is involved. (No other apps)
        """
        if (
            obj1._meta.app_label in self.route_app_labels or
            obj2._meta.app_label in self.route_app_labels
        ):
           return True
        return None
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the data app only appears in the 'content' database.
        """
        if app_label in self.route_app_labels:
            return db == 'content'
        return None

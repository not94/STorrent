# -*- coding:utf-8 -*-


class CachedProperty(property):

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        if self.fget is None:
            raise AttributeError("Unreadable attribute")
        cached_key = self.fget.__name__
        if cached_key not in instance.__dict__:
            instance.__dict__[cached_key] = self.fget(instance)
        return instance.__dict__[cached_key]

    def __set__(self, instance, value):
        if self.fset is None:
            raise AttributeError("Unset attribute")
        self.fset(instance, value)
        cached_key = self.fget.__name__
        instance.__dict__[cached_key] = self.fget(instance)

    def __delete__(self, instance):
        super(CachedProperty, self).__delete__(instance)
        del instance.__dict__[self.fget.__name__]


cached_property = CachedProperty

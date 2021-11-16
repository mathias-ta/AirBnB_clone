#!/usr/bin/python3
"""
Module contain BaseModel class of models module
"""
from uuid import uuid4, UUID
from datetime import datetime


class BaseModel():
    """
    Contain different functions and atributes for base model
    """

    def __init__(self, *args, **kwargs):
        if kwargs:
            kwargs['updated_at'] = datetime.strptime(kwargs['updated_at'],
                                                     '%Y-%m-%dT%H:%M:%S.%f')
            kwargs['created_at'] = datetime.strptime(kwargs['created_at'],
                                                     '%Y-%m-%dT%H:%M:%S.%f')
            del kwargs['__class__']
            self.__dict__.update(kwargs)
        else:
            from models import storage
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.update_at = datetime.now()
            models.storage.new(self)

    def save(self):
        from models import storage
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def __str__(self):
        class_name = type(self).__name__
        return "[{}] ({}) {}".format(class_name, self.id, self.__dict__)

    def to_dict(self):
        dic = {}
        dic.update(self.__dict__)
        dic.update({'__class__':
                   (str(type(self)).split('.')[-1]).split('\'')[0]})
        dic['created_at'] = self.created_at.isoformat()
        dic['updated_at'] = self.updated_at.isoformat()
        return dictionary

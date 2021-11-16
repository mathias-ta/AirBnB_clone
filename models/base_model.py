#!/usr/bin/python3
"""
Module contain BaseModel class of models module
"""

import models
from uuid import uuid4, UUID
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime


class BaseModel():
    """
    Contain different functions and atributes for base model
    """

    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False,
                        default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False,
                        default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        if kwargs:
            self.set_attributes(kwargs)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.utcnow()

    def set_attributes(self, attr_dict):
        """
            private: converts attr_dict values to python class attributes
        """
        if 'id' not in attr_dict:
            attr_dict['id'] = str(uuid4())
        if 'created_at' not in attr_dict:
            attr_dict['created_at'] = datetime.utcnow()
        elif not isinstance(attr_dict['created_at'], datetime):
            attr_dict['created_at'] = datetime.strptime(
                attr_dict['created_at'], "%Y-%m-%d %H:%M:%S.%f"
            )
        if 'updated_at' not in attr_dict:
            attr_dict['updated_at'] = datetime.utcnow()
        elif not isinstance(attr_dict['updated_at'], datetime):
            attr_dict['updated_at'] = datetime.strptime(
                attr_dict['updated_at'], "%Y-%m-%d %H:%M:%S.%f"
            )
        if STORAGE_TYPE != 'db':
            attr_dict.pop('__class__', None)
        for attr, val in attr_dict.items():
            setattr(self, attr, val)

    def save(self):
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def __str__(self):
        class_name = type(self).__name__
        return "[{}] ({}) {}".format(class_name, self.id, self.__dict__)

    def to_dict(self):
        dic = {}
        dic["id"] = self.id
        return dic

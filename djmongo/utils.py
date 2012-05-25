# -*- coding: utf-8 -*-
from pymongo import Connection
from bson.objectid import ObjectId

from django.db import models

from djmongo import settings

class Singleton(type):
    instance = None

    def __new__(cls, name, bases, attrs):
        '''
        If instance isn't exists generates instance
        else returns existing instance
        '''
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__new__(cls, name,
                                                         bases, attrs)
        return cls.instance


class MongoDbConnection(object):
    __metaclass__ = Singleton

    _db = None

    def __init__(self):
        connection = Connection()
        self.db = connection[settings.MONGO_DB_NAME]
    
    def get_database(self):
        '''
        Return's current db
        '''
        return self.db


def generate_collection(class_attrs):
    '''
    Generates collection in mongo 
    Gets collection name
    Checks is collection exists on mongo
    If not makes collection
    Adds _mongo_object_id field into class_attrs
    Adds _collection_name field into class_attrs
    Deletes collection form Meta class
    :param class_attrs: class attributes
    :type class_attrs: `dict`
    :return: modified class_attr
    :rtype: `dict`
    '''
    collection_name = class_attrs["Meta"].collection

    #get's collection for mongo 
    db = MongoDbConnection().get_database()

    #checks is collection exist
    if not collection_name in db.collection_names():
        db.create_collection(collection_name)

    #modified attributes
    class_attrs.update({
        '_mongo_object_id': models.CharField(verbose_name='mongo_obj_id',
                                             max_length=250,
                                             blank=True, null=True),
        '_collection_name': collection_name})

    del class_attrs["Meta"].collection

    return class_attrs

def write_into_collection(collection_name, data, object_id=None):
    '''
    Gets collection and save or insert data.
    If object_id not is None we save data,
    else we insert data
    :param collection_name: name of current collection
    :type collection: string
    :param data: Data to save into collection
    :type data: dict
    :param object_id: Object id in mongo db
    :type object_id: string
    :return: Object id
    :rtype: string
    '''
    db = MongoDbConnection().get_database()
    collection = db[collection_name]
    
    #clear _id in data if it sets by user
    if '_id' in data:
        del data['_id']

    if not object_id is None:
        obj_data = collection.find_one({'_id': ObjectId(object_id)})
        obj_data.update(data)
        write_method = getattr(collection, 'save')
    else:
        obj_data = data
        write_method = getattr(collection, 'insert')

    object_id = str(write_method(obj_data))
    
    #clear '_id' from document after writing data into mongo
    try:
        del obj_data['_id']
    except KeyError:
        pass

    return object_id


def read_from_collection(collection_name, object_id):
    '''
    Returns data from mongo by object_id without object_id
    :param collection_name: Name for current collection
    :type collection_name: String
    :param object_id: object id for current connection:
    :type object_id: string
    :return: document without object_id
    :rtype: dict
    '''
    db = MongoDbConnection().get_database()
    collection = db[collection_name]
    data = collection.find_one(ObjectId(object_id))

    if data is None:
        data = {}

    try:
        del data['_id']
    except KeyError:
        pass
    return data


def remove_from_collection(collection_name, object_id):
    '''
    Remove data from mongo by object_id.
    :param collection_name: Name for current collection
    :type collection_name: String
    :param object_id: object id for current connection
    :type object_id: string
    '''
    db = MongoDbConnection().get_database()
    collection = db[collection_name]
    collection.remove({'_id': ObjectId(object_id)})


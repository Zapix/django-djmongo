from django.db import models
from django.db.models.base import ModelBase

from djmongo.utils import generate_collection, read_from_collection, write_into_collection, remove_from_collection
from djmongo.exceptions import OnlyDictionaryCanBeSet

class NoSqlExtendModelBase(ModelBase):

    def __new__(cls, name, bases, attrs):
        meta_class = attrs.get("Meta", None)
        if meta_class and hasattr(meta_class, "collection"):
            #create collection
            attrs = generate_collection(attrs)

        return super(NoSqlExtendModelBase, cls).__new__(cls, name,
                                                        bases, attrs)


class NoSqlExtendModel(models.Model):

    __metaclass__ = NoSqlExtendModelBase

    class Meta:
        abstract = True

    _document = None

    def _load_document(self):
        '''
        Load document from mongo if has got _mongo_object_id
        :return: loaded document
        :rtype: dict
        '''
        if not self._mongo_object_id:
            return {}

        return read_from_collection(self._collection_name,
                                    self._mongo_object_id)

    @property
    def document(self):
        '''
        Get document. if not load, loaded it
        '''
        if self._document is None:
            self._document = self._load_document()
        return self._document
    
    @document.setter
    def document(self, value):
        '''
        Set's new dictionary in _document attribute
        '''
        if isinstance(value, dict):
            self._document = self.value
        else:
            raise OnlyDictionaryCanBeSet
    
    @document.deleter
    def document(self):
        '''
        Clear document
        '''
        self._document = {}

    def save(self, *args, **kwargs):
        buf = write_into_collection(self._collection_name,
                                                      self.document,
                                                      self._mongo_object_id)
        self._mongo_object_id = buf
        super(NoSqlExtendModel, self).save(*args, **kwargs)
    
    def delete(self):
        '''
        Delete document from mongo db then delete model
        '''
        remove_from_collection(self._collection_name,
                               self._mongo_object_id)
        super(NoSqlExtendModel, self).delte()


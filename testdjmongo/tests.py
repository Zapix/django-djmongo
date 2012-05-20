"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from testdjmongo import models


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class MongoModelsTest(TestCase):

    def get_new_object(self):
        return models.TestNoSqlModel(test=1)

    def test_create_object(self):
        obj = self.get_new_object()
        obj.save()
        self.assertEqual(obj.test, 1)
        self.assertTrue(obj.pk > 0)
        self.assertTrue(not '_id' in obj.document)

    def test_nosql_data(self):
        obj = self.get_new_object()
        obj.save()
        obj.document['ololo'] = 15
        obj.save()
        load_obj = models.TestNoSqlModel.objects.get(pk=obj.pk)
        self.assertEqual(load_obj.document['ololo'], obj.document['ololo'])
    
    def test_nosql_object_id(self):
        obj = self.get_new_object()
        obj.save()
        obj.document['_id'] = 'asdofasdf'
        obj.save()
        try:
            self.assertTrue(obj.document['_id'] != 'asdofasdf')
        except KeyError:
            self.assertTrue(True)


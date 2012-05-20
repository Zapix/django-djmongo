"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from djmongo import utils


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

class MongoUtilsTest(TestCase):

    def test_db_connection(self):
        '''
        Test for db connection
        '''
        db = utils.MongoDbConnection().get_database()
        self.assertTrue(not db is None)

    def test_write_data(self):
        obj_id = utils.write_into_collection('test_collection',
                                             {'test': 'test'})
        self.assertEqual(type(obj_id),str)

    def test_rewrite_data(self):
        obj_id = utils.write_into_collection('test_collection',
                                             {'test': 'test'})
        new_obj_id = utils.write_into_collection('test_collection',
                                                 {'test': 'new test'},
                                                 object_id=obj_id)

        self.assertEqual(obj_id, new_obj_id)

    def test_read_data(self):
        obj_id = utils.write_into_collection('test_collection',
                                             {'test': 'test'})
        data = utils.read_from_collection('test_collection', obj_id)
        self.assertEqual(data['test'], 'test')
        self.assertTrue(not '_id' in data)


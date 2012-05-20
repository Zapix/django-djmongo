# -*- coding: utf-8 -*-

class OnlyDictionaryCanBeSet(Exception):
    def __str__(self):
        return 'Only dictionary can be set as value for document'


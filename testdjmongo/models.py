from django.db import models
from djmongo.models import NoSqlExtendModel

class TestNoSqlModel(NoSqlExtendModel):
    test = models.IntegerField()

    class Meta:
        collection = 'test'


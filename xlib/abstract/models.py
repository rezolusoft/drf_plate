from django.db import models
from xlib.methods import uuid_gen
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404


class AbstractModelManager(models.Manager):
    def get_by_id(self, public_id):
        try:
            instance = self.get(public_id=public_id)
        except(ValueError, TypeError, ObjectDoesNotExist):
            raise Http404
        return instance


class AbstractModel(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.BooleanField(default=True)
    public_id = models.UUIDField(default=uuid_gen, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def __str__(self):
        return self.public_id

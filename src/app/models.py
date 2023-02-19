from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from django.contrib import admin


MAX_LENGTH_CUSTOMCOLLECTION_NAME = 200
MAX_LENGTH_TOKEN_NAME = 1000


class CustomUser(AbstractUser):

    def __str__(self):
        return "{}".format(self.username)

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        ordering = ["id"]


class CustomCollection(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=MAX_LENGTH_CUSTOMCOLLECTION_NAME, blank=True)
    token_count = models.IntegerField()
    date_added = models.DateField()
    last_updated = models.DateField()

    def __str__(self):
        return "Collection {}".format(self.name)

    class Meta:
        ordering = ["id"]


class Token(models.Model):
    token_id = models.CharField(max_length=200, blank=True)
    image_src = models.CharField(max_length=2000, blank=True)
    name = models.CharField(max_length=MAX_LENGTH_TOKEN_NAME, blank=True, null=True)
    collection = models.ForeignKey(CustomCollection, on_delete=models.CASCADE)
    index_in_collection = models.IntegerField(default=0)

    def __str__(self):
        return "Token {} in {}".format(self.token_id, self.collection)

    class Meta:
        ordering = ["index_in_collection", "id"]


admin.site.register(CustomUser)
admin.site.register(CustomCollection)
admin.site.register(Token)

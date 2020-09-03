from django.db import models

# Create your models here.

from django.contrib.auth.models import User, Group
from django.contrib.postgres.fields import ArrayField



class CustomPermissions(models.Model):
    objects = None  # type: None
    permission_list = ArrayField(models.TextField(blank=True, null=True))
    group = models.OneToOneField(Group, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['pk']
        db_table = 'custom_permissions'

class CrudPermissions(models.Model):
    objects = None  # type: None
    function_name = ArrayField(models.TextField(blank=True, null=True))
    name = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        db_table = 'crud_permissions'

# class UserProfile(models.Model):
#     objects = None  # type: None
#     token_key = models.CharField(max_length=128, blank=True, null=True)
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     role = models.CharField(max_length=128, blank=True, null=True, name='role')
#
#     class Meta:
#         db_table = 'user_profile'

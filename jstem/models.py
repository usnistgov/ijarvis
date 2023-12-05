from django.db import models
from django.db import models

from django.conf import settings
from django.db import models
from django.utils import timezone
from core_explore_keyword_app.permissions import rights
from core_main_app.permissions.utils import get_formatted_name

"""
class ExploreKeyword(models.Model):
    class Meta(object):
        verbose_name = "core_explore_keyword_app"
        default_permissions = ()
        permissions = (
            (
                rights.explore_keyword_access,
                get_formatted_name(rights.explore_keyword_access),
            ),
        )

"""


class Snippet(models.Model):
    name = models.CharField(max_length=200)
    body=models.TextField()

    def __str__(self):
        return self.name

# Create your models here.

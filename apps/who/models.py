import logging
import requests
import os

from uuid import uuid4

from django.db import models
from django.contrib.auth.models import AbstractBaseUser

logger = logging.getLogger(__name__)

# UserInfo model to store results from Twitch API get user info calls
class UserInfo(models.Model):
    info = models.JSONField(blank=True, null=True)
    uid = models.PositiveIntegerField(unique=True, default=None)
    login = models.CharField(max_length=30, primary_key=True)

    # twitch results return as dict->list->dict so get rid of the first dict and the list
    def save(self, *args, **kwargs):
        self.info = self.info['data'][0]
        self.uid = int(self.info['id'])
        self.login = self.info['login']
        logger.info('saving info as {}'.format(self.info))
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.login)

    #def get_absolute_url(self):
    #    return reverse("model_detail", kwargs={"pk": self.pk})
    
    class Meta:
        verbose_name = "user info"

# not currently in use
class WhoUser(AbstractBaseUser):
    uid = models.UUIDField(primary_key=True, max_length=255, default=uuid4)
    password = None

    USERNAME_FIELD = "uid"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.uid

    class Meta:
        verbose_name = "custom auth user"
        #db_table = "auth_user"

# not currently in use
class OAuthToken(models.Model):
    user_id = models.OneToOneField(WhoUser, on_delete=models.CASCADE, primary_key=True)
    token = models.TextField()
    token_refresh = models.TextField()
    expires_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.token

    class Meta:
        verbose_name = "oauth2 token"
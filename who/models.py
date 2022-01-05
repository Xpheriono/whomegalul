import logging

from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractBaseUser

logger = logging.getLogger('django')

# UserInfo model to store results from Twitch API get user info calls
class UserInfo(models.Model):
    info = models.JSONField(blank=True, null=True)
    uid = models.PositiveIntegerField(unique=True, default=None)
    login = models.CharField(max_length=30, primary_key=True)

    # 2008-06-14T06:12:52.461775Z 
    # twitch results return as dict->list->dict so get rid of the first dict and the list
    def save(self, *args, **kwargs):
        self.info = self.info['data'][0]
        self.uid = int(self.info['id'])
        self.login = self.info['login']
        created_at = datetime.strptime(self.info['created_at'],'%Y-%m-%dT%H:%M:%S%z')
        self.info['created_at'] = created_at.strftime('%b %d %Y %I:%M %p')
        self.info['user_page'] = 'https://twitch.tv/' + self.login
        self.info['view_count'] = '{:,}'.format(self.info['view_count'])
        
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.login)
    
    class Meta:
        verbose_name = "user info"
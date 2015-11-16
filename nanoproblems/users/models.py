from django.db import models
import uuid

NANODEGREE_CHOICES = (('FULLSTACK', 'FullStack Developer'),
                      ('FRONTEND', 'Frontend Developer'),
                      ('ANDROID', 'Android Developer'),
                      ('DATA ANALYST', 'Data Analyst'),
                      ('IOS DEVELOPER', 'IOS Developer'))


class User(models.Model):

    """ User Information. """
    email = models.EmailField(max_length=100, default="")
    nickname = models.CharField(max_length=50, default="")
    user_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nanodegree = models.CharField(max_length=15,
                                  choices=NANODEGREE_CHOICES, default='Developer')

    def __unicode__(self):
        """ Return the username to better id the object. """
        return self.nickname

    def natural_key(self):
        return (self.email, self.nickname)

    class Meta:
        unique_together = (('email', 'nickname'))

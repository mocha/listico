from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Tasklist(models.Model):
  title = models.CharField(max_length=50)
  added_on = models.DateTimeField(auto_now_add=True)
  user = models.ForeignKey(User, null=True, blank=True, related_name='tasklists')
          
  def __unicode__(self):
    return u'%s' % (self.title)
  def __str__(self):
    return self.title
  class Meta:
    ordering = ["title"]

class Listitem(models.Model):
  title = models.CharField(max_length=255)
  added_on = models.DateTimeField(auto_now_add=True)
  complete = models.BooleanField(default=False)
  completed_on = models.DateTimeField(null=True)
  deleted = models.BooleanField(default=False)
  deleted_on = models.DateTimeField(null=True)
  tasklist = models.ForeignKey(Tasklist)
  def __unicode__(self):
    return u'%s' % (self.title)
  def __str__(self):
    return self.title
  class Meta:
    ordering = ["title"]

class UserProfile(models.Model):
  user = models.OneToOneField(User, unique=True)
  current_list = models.ForeignKey(Tasklist, null=True, blank=True, default=None)
  def __unicode__(self):
    return u'%s' % (self.user.email)
  def __str__(self):
    return self.user.email
  class Meta:
    ordering = ["user__email"]


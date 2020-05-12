from django.db import models

from user.models import User

# Create your models here.

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null = True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)                          

    def __str__(self):
        return "%s -> %s" % (self.author.name, self.content)
    
    class Meta:
        db_table = 'comments'


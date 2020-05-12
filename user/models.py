from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=50, unique=True)     
    email = models.CharField(max_length=50, unique=True)    
    password = models.CharField(max_length=300)          # sqlite3에서는 글자 수 초과해도 되지만, MySQL에서는 초과하면 에러가 남.
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'users'




